import json
import os
import urllib.error
import urllib.request

from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import permissions, response, status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.views import APIView

from api.serializers import BaseContentSerializer
from cms.models import BaseContent


def _truncate_text(value: object, max_length: int = 400) -> str:
	text = str(value or "").strip()
	if len(text) <= max_length:
		return text
	return f"{text[:max_length]}..."


def _compact_listing_context(listing_context: dict) -> dict:
	metadata = listing_context.get("metadata") if isinstance(listing_context, dict) else {}
	if not isinstance(metadata, dict):
		metadata = {}

	blocks = listing_context.get("blocks") if isinstance(listing_context, dict) else []
	if not isinstance(blocks, list):
		blocks = []

	images = listing_context.get("images") if isinstance(listing_context, dict) else []
	if not isinstance(images, list):
		images = []

	compact_metadata: dict[str, str] = {}
	for key, value in list(metadata.items())[:30]:
		compact_metadata[_truncate_text(key, 60)] = _truncate_text(value, 120)

	compact_blocks: list[dict[str, object]] = []
	for block in blocks[:8]:
		if not isinstance(block, dict):
			continue
		compact_blocks.append(
			{
				"block_type": block.get("block_type"),
				"title": _truncate_text(block.get("title"), 140),
				"body": _truncate_text(block.get("body"), 260),
				"position": block.get("position"),
			}
		)

	compact_images: list[dict[str, object]] = []
	for image in images[:12]:
		if not isinstance(image, dict):
			continue
		compact_images.append(
			{
				"alt_text": _truncate_text(image.get("alt_text"), 120),
				"caption": _truncate_text(image.get("caption"), 180),
				"is_primary": image.get("is_primary"),
				"sort_order": image.get("sort_order"),
			}
		)

	return {
		"id": listing_context.get("id"),
		"slug": listing_context.get("slug"),
		"title": _truncate_text(listing_context.get("title"), 180),
		"industry": listing_context.get("industry"),
		"status": listing_context.get("status"),
		"description": _truncate_text(listing_context.get("description"), 500),
		"metadata": compact_metadata,
		"real_estate_details": listing_context.get("real_estate_details"),
		"product_details": listing_context.get("product_details"),
		"blocks": compact_blocks,
		"images": compact_images,
	}


class HealthCheckView(APIView):
	permission_classes = [permissions.AllowAny]

	def get(
		self,
		request: Request,
		*args: object,
		**kwargs: object,
	) -> response.Response:
		payload = {
			"status": "ok",
			"service": "cms-ygen-backend",
			"timestamp": timezone.now().isoformat(),
		}
		return response.Response(payload)


class ContentListView(ListAPIView):
	serializer_class = BaseContentSerializer
	permission_classes = [permissions.AllowAny]

	def get_queryset(self) -> QuerySet[BaseContent]:
		return (
			BaseContent.objects.select_related("owner", "real_estate_details", "product_details")
			.prefetch_related("blocks", "images", "meta_items")
			.order_by("-updated_at")
		)


class AIChatView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(
		self,
		request: Request,
		*args: object,
		**kwargs: object,
	) -> response.Response:
		message = request.data.get("message")
		listing_context = request.data.get("listing_context")
		history = request.data.get("history", [])

		if not isinstance(message, str) or not message.strip():
			return response.Response(
				{"detail": "message is required."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		if not isinstance(listing_context, dict):
			return response.Response(
				{"detail": "listing_context must be an object."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		if not isinstance(history, list):
			history = []

		api_key = os.getenv("GROQ_API_KEY", "")
		if not api_key:
			return response.Response(
				{"detail": "GROQ_API_KEY is missing from environment."},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR,
			)

		model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
		max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "220"))

		system_prompt = (
			"You are a listing assistant for a CMS showcase. "
			"Answer only from the provided listing context. "
			"If information is missing, clearly say it is not present in the listing data. "
			"Be concise, factual, and helpful."
		)

		compact_context = _compact_listing_context(listing_context)
		serialized_context = json.dumps(compact_context, ensure_ascii=True)
		messages: list[dict[str, str]] = [
			{"role": "system", "content": system_prompt},
			{
				"role": "system",
				"content": f"Listing context JSON:\n{serialized_context}",
			},
		]

		for item in history[-4:]:
			if not isinstance(item, dict):
				continue
			role = item.get("role")
			content = item.get("content")
			if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
				messages.append({"role": role, "content": _truncate_text(content, 420)})

		messages.append({"role": "user", "content": message.strip()})

		payload = {
			"model": model,
			"temperature": 0.2,
			"max_tokens": max_tokens,
			"messages": messages,
		}

		req = urllib.request.Request(
			url="https://api.groq.com/openai/v1/chat/completions",
			data=json.dumps(payload).encode("utf-8"),
			headers={
				"Authorization": f"Bearer {api_key}",
				"Content-Type": "application/json",
				"Accept": "application/json",
				"User-Agent": "cms-ygen-backend/1.0",
			},
			method="POST",
		)

		try:
			with urllib.request.urlopen(req, timeout=20) as groq_response:
				raw_body = groq_response.read().decode("utf-8")
		except urllib.error.HTTPError as exc:
			error_body = exc.read().decode("utf-8", errors="replace")
			return response.Response(
				{
					"detail": "Groq request failed.",
					"status_code": exc.code,
					"error": error_body,
				},
				status=status.HTTP_502_BAD_GATEWAY,
			)
		except urllib.error.URLError as exc:
			return response.Response(
				{"detail": "Failed to reach Groq.", "error": str(exc.reason)},
				status=status.HTTP_502_BAD_GATEWAY,
			)

		try:
			parsed = json.loads(raw_body)
		except json.JSONDecodeError:
			return response.Response(
				{"detail": "Groq returned invalid JSON."},
				status=status.HTTP_502_BAD_GATEWAY,
			)

		choices = parsed.get("choices")
		if not isinstance(choices, list) or len(choices) == 0:
			return response.Response(
				{"detail": "Groq response did not include choices."},
				status=status.HTTP_502_BAD_GATEWAY,
			)

		first = choices[0]
		assistant_message = first.get("message", {}) if isinstance(first, dict) else {}
		assistant_content = assistant_message.get("content")

		if not isinstance(assistant_content, str) or not assistant_content.strip():
			return response.Response(
				{"detail": "Groq response did not include assistant content."},
				status=status.HTTP_502_BAD_GATEWAY,
			)

		return response.Response(
			{
				"reply": assistant_content.strip(),
				"model": parsed.get("model", model),
			}
		)

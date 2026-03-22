from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import permissions, response
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.views import APIView

from api.serializers import BaseContentSerializer
from cms.models import BaseContent


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
			BaseContent.objects.select_related("owner")
			.prefetch_related("blocks", "images")
			.order_by("-updated_at")
		)

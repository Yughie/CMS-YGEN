from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ContentStatus(models.TextChoices):
	DRAFT = "draft", "Draft"
	PUBLISHED = "published", "Published"
	ARCHIVED = "archived", "Archived"


class IndustryType(models.TextChoices):
	REAL_ESTATE = "real_estate", "Real Estate"
	PRODUCT = "product", "Product"


class ContentBlockType(models.TextChoices):
	RICH_TEXT = "rich_text", "Rich Text"
	HERO = "hero", "Hero"
	GALLERY = "gallery", "Gallery"
	CTA = "cta", "Call To Action"


class CtaStyle(models.TextChoices):
	PRIMARY = "primary", "Primary"
	SECONDARY = "secondary", "Secondary"
	GHOST = "ghost", "Ghost"


class CtaTarget(models.TextChoices):
	SELF = "_self", "Same Tab"
	BLANK = "_blank", "New Tab"


class BaseContent(models.Model):
	title = models.CharField(
		max_length=255,
		help_text="Public title shown on listings and detail pages.",
	)
	description = models.TextField(
		blank=True,
		help_text="Long-form summary to describe this content item.",
	)
	slug = models.SlugField(
		unique=True,
		help_text="URL-safe unique identifier, e.g. modern-family-home.",
	)
	industry = models.CharField(
		max_length=32,
		choices=IndustryType.choices,
		help_text="Industry type that controls which detail model should be attached.",
	)
	status = models.CharField(
		max_length=16,
		choices=ContentStatus.choices,
		default=ContentStatus.DRAFT,
		help_text="Publishing state of this content.",
	)
	publish_at = models.DateTimeField(
		blank=True,
		null=True,
		help_text="When content becomes visible. Required for published status.",
	)
	unpublish_at = models.DateTimeField(
		blank=True,
		null=True,
		help_text="Optional end date/time. Must be later than publish date/time.",
	)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		related_name="owned_contents",
		blank=True,
		null=True,
		help_text="Optional owner reference. Can be left empty for single-admin workflow.",
	)
	excerpt = models.CharField(
		max_length=500,
		blank=True,
		help_text="Short teaser text for cards and list previews.",
	)
	body = models.TextField(
		blank=True,
		help_text="Main body content. Can be used together with blocks.",
	)
	seo_title = models.CharField(
		max_length=255,
		blank=True,
		help_text="Optional SEO title. Falls back to title when empty.",
	)
	seo_description = models.CharField(
		max_length=500,
		blank=True,
		help_text="Optional SEO description for meta tags.",
	)
	metadata = models.JSONField(
		default=dict,
		blank=True,
		help_text="Flexible JSON object for extra machine-readable fields.",
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]
		constraints = [
			models.CheckConstraint(
				condition=(
					models.Q(unpublish_at__isnull=True)
					| models.Q(publish_at__isnull=True)
					| models.Q(unpublish_at__gt=models.F("publish_at"))
				),
				name="cms_content_valid_publish_window",
			),
		]
		indexes = [
			models.Index(fields=["industry", "status"]),
			models.Index(fields=["status", "publish_at"]),
		]

	def clean(self) -> None:
		if self.publish_at and self.unpublish_at and self.unpublish_at <= self.publish_at:
			raise ValidationError(
				{"unpublish_at": "Unpublish datetime must be later than publish datetime."}
			)
		if self.status == ContentStatus.PUBLISHED and self.publish_at is None:
			raise ValidationError(
				{"publish_at": "Published content requires a publish datetime."}
			)

	def is_currently_published(self) -> bool:
		now = timezone.now()
		if self.status != ContentStatus.PUBLISHED:
			return False
		if self.publish_at and now < self.publish_at:
			return False
		if self.unpublish_at and now >= self.unpublish_at:
			return False
		return True

	def __str__(self) -> str:
		return f"{self.title} ({self.industry})"


class ContentMetaItem(models.Model):
	content = models.ForeignKey(
		BaseContent,
		on_delete=models.CASCADE,
		related_name="meta_items",
		help_text="Parent content item for this metadata entry.",
	)
	key = models.CharField(
		max_length=100,
		help_text="Metadata key, e.g. city, category, listing_type.",
	)
	value = models.CharField(
		max_length=255,
		help_text="Metadata value as plain text.",
	)

	class Meta:
		ordering = ["content_id", "key"]
		constraints = [
			models.UniqueConstraint(
				fields=["content", "key"],
				name="cms_contentmetaitem_unique_key_per_content",
			),
		]

	def __str__(self) -> str:
		return f"Meta<{self.content.slug}:{self.key}>"


class ContentBlock(models.Model):
	content = models.ForeignKey(
		BaseContent,
		on_delete=models.CASCADE,
		related_name="blocks",
		help_text="Parent content item for this block.",
	)
	block_type = models.CharField(
		max_length=32,
		choices=ContentBlockType.choices,
		help_text="Block renderer type used by the frontend.",
	)
	title = models.CharField(
		max_length=255,
		blank=True,
		help_text="Optional block heading.",
	)
	body = models.TextField(
		blank=True,
		help_text="Optional rich text/body copy for this block.",
	)
	payload = models.JSONField(
		default=dict,
		blank=True,
		help_text='JSON object for block config, e.g. {"cta_label": "Book now", "cta_href": "/contact"}.',
	)
	cta_label = models.CharField(
		max_length=120,
		blank=True,
		help_text="CTA button label. Recommended for CTA block type.",
	)
	cta_href = models.CharField(
		max_length=500,
		blank=True,
		help_text="CTA destination URL/path, e.g. /contact.",
	)
	cta_style = models.CharField(
		max_length=20,
		choices=CtaStyle.choices,
		default=CtaStyle.PRIMARY,
		help_text="CTA visual style used by frontend.",
	)
	cta_target = models.CharField(
		max_length=10,
		choices=CtaTarget.choices,
		default=CtaTarget.SELF,
		help_text="Open link in same tab or new tab.",
	)
	position = models.PositiveIntegerField(
		default=0,
		help_text="Display order within this content item. Must be unique per content.",
	)
	is_active = models.BooleanField(
		default=True,
		help_text="Turn block visibility on/off without deleting it.",
	)

	class Meta:
		ordering = ["content_id", "position", "id"]
		constraints = [
			models.UniqueConstraint(
				fields=["content", "position"],
				name="cms_contentblock_unique_position_per_content",
			),
		]
		indexes = [
			models.Index(fields=["content", "position"]),
			models.Index(fields=["content", "is_active"]),
		]

	def clean(self) -> None:
		if not isinstance(self.payload, dict):
			raise ValidationError({"payload": "Payload must be a JSON object."})
		if self.block_type == ContentBlockType.CTA:
			if not self.cta_label:
				raise ValidationError({"cta_label": "CTA block requires button label."})
			if not self.cta_href:
				raise ValidationError({"cta_href": "CTA block requires destination URL/path."})

	def resolved_payload(self) -> dict:
		data = dict(self.payload or {})
		if self.cta_label:
			data["cta_label"] = self.cta_label
		if self.cta_href:
			data["cta_href"] = self.cta_href
		if self.cta_style:
			data["cta_style"] = self.cta_style
		if self.cta_target:
			data["cta_target"] = self.cta_target
		return data

	def __str__(self) -> str:
		return f"Block<{self.content.slug}:{self.block_type}:{self.position}>"


class ContentImage(models.Model):
	content = models.ForeignKey(
		BaseContent,
		on_delete=models.CASCADE,
		related_name="images",
		help_text="Parent content item for this image.",
	)
	image = models.ImageField(
		upload_to="cms/images/%Y/%m/%d",
		help_text="Upload image file. Stored under media/cms/images/...")
	alt_text = models.CharField(
		max_length=255,
		help_text="Accessibility description of the image.",
	)
	caption = models.CharField(
		max_length=500,
		blank=True,
		help_text="Optional caption shown under the image.",
	)
	sort_order = models.PositiveIntegerField(
		default=0,
		help_text="Display order among images for this content.",
	)
	is_primary = models.BooleanField(
		default=False,
		help_text="Mark as the main/cover image. Only one primary image is allowed per content.",
	)

	class Meta:
		ordering = ["content_id", "sort_order", "id"]
		constraints = [
			models.UniqueConstraint(
				fields=["content"],
				condition=models.Q(is_primary=True),
				name="cms_contentimage_single_primary_per_content",
			),
		]
		indexes = [
			models.Index(fields=["content", "sort_order"]),
		]

	def __str__(self) -> str:
		return f"Image<{self.content.slug}:{self.id}>"


class RealEstateDetails(models.Model):
	content = models.OneToOneField(
		BaseContent,
		on_delete=models.CASCADE,
		related_name="real_estate_details",
		help_text="Linked base content. Industry must be Real Estate.",
	)
	listing_price = models.DecimalField(
		max_digits=12,
		decimal_places=2,
		help_text="Listing price for the property.",
	)
	currency = models.CharField(
		max_length=3,
		default="USD",
		help_text="ISO currency code, e.g. USD.",
	)
	bedrooms = models.PositiveSmallIntegerField(
		default=0,
		help_text="Number of bedrooms.",
	)
	bathrooms = models.DecimalField(
		max_digits=4,
		decimal_places=1,
		default=Decimal("1.0"),
		help_text="Number of bathrooms. Supports halves, e.g. 2.5.",
	)
	area_sqft = models.PositiveIntegerField(
		blank=True,
		null=True,
		help_text="Optional interior area in square feet.",
	)
	address_line = models.CharField(
		max_length=255,
		help_text="Property street address line.",
	)

	def clean(self) -> None:
		if self.content.industry != IndustryType.REAL_ESTATE:
			raise ValidationError(
				{"content": "Real estate details can only attach to real estate content."}
			)

	def __str__(self) -> str:
		return f"RealEstate<{self.content.slug}>"


class ProductDetails(models.Model):
	content = models.OneToOneField(
		BaseContent,
		on_delete=models.CASCADE,
		related_name="product_details",
		help_text="Linked base content. Industry must be Product.",
	)
	sku = models.CharField(
		max_length=100,
		unique=True,
		help_text="Unique stock-keeping unit identifier.",
	)
	price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		help_text="Product price.",
	)
	stock_quantity = models.PositiveIntegerField(
		default=0,
		help_text="Current stock quantity available.",
	)

	def clean(self) -> None:
		if self.content.industry != IndustryType.PRODUCT:
			raise ValidationError(
				{"content": "Product details can only attach to product content."}
			)

	def __str__(self) -> str:
		return f"Product<{self.sku}>"

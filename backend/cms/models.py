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


class BaseContent(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	slug = models.SlugField(unique=True)
	industry = models.CharField(max_length=32, choices=IndustryType.choices)
	status = models.CharField(
		max_length=16,
		choices=ContentStatus.choices,
		default=ContentStatus.DRAFT,
	)
	publish_at = models.DateTimeField(blank=True, null=True)
	unpublish_at = models.DateTimeField(blank=True, null=True)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		related_name="owned_contents",
		blank=True,
		null=True,
	)
	excerpt = models.CharField(max_length=500, blank=True)
	body = models.TextField(blank=True)
	seo_title = models.CharField(max_length=255, blank=True)
	seo_description = models.CharField(max_length=500, blank=True)
	metadata = models.JSONField(default=dict, blank=True)
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


class ContentBlock(models.Model):
	content = models.ForeignKey(
		BaseContent,
		on_delete=models.CASCADE,
		related_name="blocks",
	)
	block_type = models.CharField(max_length=32, choices=ContentBlockType.choices)
	title = models.CharField(max_length=255, blank=True)
	body = models.TextField(blank=True)
	payload = models.JSONField(default=dict, blank=True)
	position = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)

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

	def __str__(self) -> str:
		return f"Block<{self.content.slug}:{self.block_type}:{self.position}>"


class ContentImage(models.Model):
	content = models.ForeignKey(
		BaseContent,
		on_delete=models.CASCADE,
		related_name="images",
	)
	image = models.ImageField(upload_to="cms/images/%Y/%m/%d")
	alt_text = models.CharField(max_length=255)
	caption = models.CharField(max_length=500, blank=True)
	sort_order = models.PositiveIntegerField(default=0)
	is_primary = models.BooleanField(default=False)

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
	)
	listing_price = models.DecimalField(max_digits=12, decimal_places=2)
	currency = models.CharField(max_length=3, default="USD")
	bedrooms = models.PositiveSmallIntegerField(default=0)
	bathrooms = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal("1.0"))
	area_sqft = models.PositiveIntegerField(blank=True, null=True)
	address_line = models.CharField(max_length=255)

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
	)
	sku = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock_quantity = models.PositiveIntegerField(default=0)

	def clean(self) -> None:
		if self.content.industry != IndustryType.PRODUCT:
			raise ValidationError(
				{"content": "Product details can only attach to product content."}
			)

	def __str__(self) -> str:
		return f"Product<{self.sku}>"

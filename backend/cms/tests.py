from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from cms.models import (
	BaseContent,
	ContentBlock,
	ContentBlockType,
	ContentImage,
	ContentMetaItem,
	ContentStatus,
	IndustryType,
	ProductDetails,
	RealEstateDetails,
)


class BaseContentValidationTests(TestCase):
	def test_published_content_requires_publish_datetime(self) -> None:
		content = BaseContent(
			title="Published",
			slug="published",
			industry=IndustryType.PRODUCT,
			status=ContentStatus.PUBLISHED,
		)

		with self.assertRaises(ValidationError):
			content.full_clean()

	def test_invalid_publish_window_raises_validation_error(self) -> None:
		now = timezone.now()
		content = BaseContent(
			title="Invalid Window",
			slug="invalid-window",
			industry=IndustryType.REAL_ESTATE,
			status=ContentStatus.DRAFT,
			publish_at=now,
			unpublish_at=now,
		)

		with self.assertRaises(ValidationError):
			content.full_clean()


class IndustryExtensionValidationTests(TestCase):
	def test_real_estate_extension_enforces_industry_match(self) -> None:
		content = BaseContent.objects.create(
			title="Product Content",
			slug="product-content",
			industry=IndustryType.PRODUCT,
			status=ContentStatus.DRAFT,
		)
		details = RealEstateDetails(
			content=content,
			listing_price=250000,
			address_line="123 Main St",
		)

		with self.assertRaises(ValidationError):
			details.full_clean()


class DynamicContentAndImageTests(TestCase):
	def test_cta_block_exposes_structured_payload_values(self) -> None:
		content = BaseContent.objects.create(
			title="CTA Content",
			description="CTA content",
			slug="cta-content",
			industry=IndustryType.PRODUCT,
			status=ContentStatus.DRAFT,
		)
		block = ContentBlock.objects.create(
			content=content,
			block_type=ContentBlockType.CTA,
			cta_label="Book now",
			cta_href="/contact",
		)

		self.assertEqual(
			block.resolved_payload(),
			{
				"cta_label": "Book now",
				"cta_href": "/contact",
				"cta_style": "primary",
				"cta_target": "_self",
			},
		)

	def test_content_meta_item_unique_key_per_content(self) -> None:
		content = BaseContent.objects.create(
			title="Meta Content",
			description="Meta content",
			slug="meta-content",
			industry=IndustryType.PRODUCT,
			status=ContentStatus.DRAFT,
		)
		ContentMetaItem.objects.create(content=content, key="city", value="New York")

		with self.assertRaises(IntegrityError):
			ContentMetaItem.objects.create(content=content, key="city", value="Boston")

	def test_content_block_payload_must_be_json_object(self) -> None:
		content = BaseContent.objects.create(
			title="Article",
			description="Long-form content",
			slug="article",
			industry=IndustryType.PRODUCT,
			status=ContentStatus.DRAFT,
		)
		block = ContentBlock(
			content=content,
			block_type=ContentBlockType.RICH_TEXT,
			payload=["invalid", "list"],
		)

		with self.assertRaises(ValidationError):
			block.full_clean()

	def test_only_one_primary_image_per_content(self) -> None:
		content = BaseContent.objects.create(
			title="Property",
			description="Property with photos",
			slug="property",
			industry=IndustryType.REAL_ESTATE,
			status=ContentStatus.DRAFT,
		)
		ContentImage.objects.create(
			content=content,
			image="cms/images/2026/03/22/first.jpg",
			alt_text="Front view",
			is_primary=True,
		)

		with self.assertRaises(IntegrityError):
			ContentImage.objects.create(
				content=content,
				image="cms/images/2026/03/22/second.jpg",
				alt_text="Back view",
				is_primary=True,
			)

	def test_product_extension_enforces_industry_match(self) -> None:
		content = BaseContent.objects.create(
			title="House",
			slug="house",
			industry=IndustryType.REAL_ESTATE,
			status=ContentStatus.DRAFT,
		)
		details = ProductDetails(
			content=content,
			sku="SKU-001",
			price=19.99,
			stock_quantity=5,
		)

		with self.assertRaises(ValidationError):
			details.full_clean()


class SeedSampleContentCommandTests(TestCase):
	def test_seed_sample_content_creates_expected_records(self) -> None:
		call_command("seed_sample_content")

		self.assertEqual(BaseContent.objects.count(), 2)
		self.assertEqual(RealEstateDetails.objects.count(), 1)
		self.assertEqual(ProductDetails.objects.count(), 1)
		self.assertEqual(ContentBlock.objects.count(), 6)
		self.assertEqual(ContentImage.objects.count(), 4)

	def test_seed_sample_content_reset_replaces_existing_data(self) -> None:
		BaseContent.objects.create(
			title="Old",
			description="Old content",
			slug="old-content",
			industry=IndustryType.PRODUCT,
			status=ContentStatus.DRAFT,
		)

		call_command("seed_sample_content", reset=True)

		slugs = sorted(BaseContent.objects.values_list("slug", flat=True))
		self.assertEqual(slugs, ["modern-family-home", "pro-espresso-machine-x2"])

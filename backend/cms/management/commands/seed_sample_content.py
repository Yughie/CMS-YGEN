from decimal import Decimal
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils import timezone

from cms.models import (
    BaseContent,
    ContentBlock,
    ContentBlockType,
    ContentImage,
    ContentStatus,
    IndustryType,
    ProductDetails,
    RealEstateDetails,
)


class Command(BaseCommand):
    help = "Seed sample CMS content for real estate and product pages."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing CMS content before seeding.",
        )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        should_reset = bool(options.get("reset", False))
        if should_reset:
            self._reset_data()

        seeded_count = 0
        seeded_count += self._seed_real_estate_content()
        seeded_count += self._seed_product_content()

        self.stdout.write(
            self.style.SUCCESS(f"Sample CMS content generated. Items upserted: {seeded_count}")
        )

    def _reset_data(self) -> None:
        ContentImage.objects.all().delete()
        ContentBlock.objects.all().delete()
        ProductDetails.objects.all().delete()
        RealEstateDetails.objects.all().delete()
        BaseContent.objects.all().delete()
        self.stdout.write(self.style.WARNING("Existing CMS content deleted."))

    def _seed_real_estate_content(self) -> int:
        now = timezone.now()
        content, _ = BaseContent.objects.update_or_create(
            slug="modern-family-home",
            defaults={
                "title": "Modern Family Home in Westview",
                "description": "A turnkey 4-bedroom home with open-plan living and private garden.",
                "industry": IndustryType.REAL_ESTATE,
                "status": ContentStatus.PUBLISHED,
                "publish_at": now,
                "excerpt": "Move-in ready property in a quiet residential neighborhood.",
                "body": "This home includes a renovated kitchen, natural light throughout, and a dedicated office space.",
                "seo_title": "Modern Family Home in Westview | CMS-YGEN",
                "seo_description": "Explore a 4-bedroom modern family home with updated interiors and flexible living spaces.",
                "metadata": {"city": "Westview", "listing_type": "sale"},
            },
        )

        RealEstateDetails.objects.update_or_create(
            content=content,
            defaults={
                "listing_price": Decimal("725000.00"),
                "currency": "USD",
                "bedrooms": 4,
                "bathrooms": Decimal("2.5"),
                "area_sqft": 2380,
                "address_line": "1458 Cedar Ridge Ave",
            },
        )

        ContentBlock.objects.filter(content=content).delete()
        ContentBlock.objects.bulk_create(
            [
                ContentBlock(
                    content=content,
                    block_type=ContentBlockType.HERO,
                    title="Spacious family living",
                    body="A bright, modern home with premium finishes.",
                    payload={"cta_label": "Schedule Tour", "cta_href": "/contact"},
                    position=1,
                    is_active=True,
                ),
                ContentBlock(
                    content=content,
                    block_type=ContentBlockType.RICH_TEXT,
                    title="Highlights",
                    body="Updated kitchen, hardwood floors, and a landscaped backyard.",
                    payload={"columns": 2},
                    position=2,
                    is_active=True,
                ),
                ContentBlock(
                    content=content,
                    block_type=ContentBlockType.GALLERY,
                    title="Property Gallery",
                    body="",
                    payload={"layout": "masonry"},
                    position=3,
                    is_active=True,
                ),
            ]
        )

        ContentImage.objects.filter(content=content).delete()
        ContentImage.objects.bulk_create(
            [
                ContentImage(
                    content=content,
                    image="cms/images/sample/real-estate-front.jpg",
                    alt_text="Front exterior of modern family home",
                    caption="Street view",
                    sort_order=1,
                    is_primary=True,
                ),
                ContentImage(
                    content=content,
                    image="cms/images/sample/real-estate-living.jpg",
                    alt_text="Open-plan living room",
                    caption="Main living area",
                    sort_order=2,
                    is_primary=False,
                ),
            ]
        )
        return 1

    def _seed_product_content(self) -> int:
        now = timezone.now()
        content, _ = BaseContent.objects.update_or_create(
            slug="pro-espresso-machine-x2",
            defaults={
                "title": "Pro Espresso Machine X2",
                "description": "Commercial-grade espresso performance designed for home and boutique cafes.",
                "industry": IndustryType.PRODUCT,
                "status": ContentStatus.PUBLISHED,
                "publish_at": now,
                "excerpt": "Precision temperature control and dual-boiler workflow.",
                "body": "The X2 delivers consistent extraction with programmable profiles and a compact stainless design.",
                "seo_title": "Pro Espresso Machine X2 | CMS-YGEN",
                "seo_description": "Discover barista-level espresso quality with dual boilers and profile tuning.",
                "metadata": {"category": "appliances", "brand": "YGEN"},
            },
        )

        ProductDetails.objects.update_or_create(
            content=content,
            defaults={
                "sku": "X2-ESP-001",
                "price": Decimal("1499.00"),
                "stock_quantity": 24,
            },
        )

        ContentBlock.objects.filter(content=content).delete()
        ContentBlock.objects.bulk_create(
            [
                ContentBlock(
                    content=content,
                    block_type=ContentBlockType.HERO,
                    title="Barista quality at home",
                    body="Engineered for reliable pressure and thermal consistency.",
                    payload={"cta_label": "Buy Now", "cta_href": "/checkout"},
                    position=1,
                    is_active=True,
                ),
                ContentBlock(
                    content=content,
                    block_type=ContentBlockType.RICH_TEXT,
                    title="Technical Specs",
                    body="Dual boiler, PID temperature control, and pre-infusion support.",
                    payload={"specs": ["Dual Boiler", "PID", "58mm Portafilter"]},
                    position=2,
                    is_active=True,
                ),
                ContentBlock(
                    content=content,
                    block_type=ContentBlockType.CTA,
                    title="Need a bundle?",
                    body="Save more with grinder + machine combo packages.",
                    payload={"cta_label": "View Bundles", "cta_href": "/bundles"},
                    position=3,
                    is_active=True,
                ),
            ]
        )

        ContentImage.objects.filter(content=content).delete()
        ContentImage.objects.bulk_create(
            [
                ContentImage(
                    content=content,
                    image="cms/images/sample/product-main.jpg",
                    alt_text="Pro Espresso Machine X2 product hero image",
                    caption="Front product shot",
                    sort_order=1,
                    is_primary=True,
                ),
                ContentImage(
                    content=content,
                    image="cms/images/sample/product-detail.jpg",
                    alt_text="Close-up of espresso machine controls",
                    caption="Control panel detail",
                    sort_order=2,
                    is_primary=False,
                ),
            ]
        )
        return 1

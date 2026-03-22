# Generated manually for initial CMS schema setup.

from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                (
                    "industry",
                    models.CharField(
                        choices=[
                            ("real_estate", "Real Estate"),
                            ("product", "Product"),
                        ],
                        max_length=32,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("published", "Published"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=16,
                    ),
                ),
                ("publish_at", models.DateTimeField(blank=True, null=True)),
                ("unpublish_at", models.DateTimeField(blank=True, null=True)),
                ("excerpt", models.CharField(blank=True, max_length=500)),
                ("body", models.TextField(blank=True)),
                ("seo_title", models.CharField(blank=True, max_length=255)),
                (
                    "seo_description",
                    models.CharField(blank=True, max_length=500),
                ),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="owned_contents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="ProductDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sku", models.CharField(max_length=100, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock_quantity", models.PositiveIntegerField(default=0)),
                (
                    "content",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_details",
                        to="cms.basecontent",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RealEstateDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "listing_price",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                ("currency", models.CharField(default="USD", max_length=3)),
                ("bedrooms", models.PositiveSmallIntegerField(default=0)),
                (
                    "bathrooms",
                    models.DecimalField(
                        decimal_places=1,
                        default=Decimal("1.0"),
                        max_digits=4,
                    ),
                ),
                ("area_sqft", models.PositiveIntegerField(blank=True, null=True)),
                ("address_line", models.CharField(max_length=255)),
                (
                    "content",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="real_estate_details",
                        to="cms.basecontent",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="basecontent",
            index=models.Index(fields=["industry", "status"], name="cms_basecon_industr_5570b2_idx"),
        ),
        migrations.AddIndex(
            model_name="basecontent",
            index=models.Index(fields=["status", "publish_at"], name="cms_basecon_status_98a198_idx"),
        ),
        migrations.AddConstraint(
            model_name="basecontent",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(unpublish_at__isnull=True)
                    | models.Q(publish_at__isnull=True)
                    | models.Q(unpublish_at__gt=models.F("publish_at"))
                ),
                name="cms_content_valid_publish_window",
            ),
        ),
    ]

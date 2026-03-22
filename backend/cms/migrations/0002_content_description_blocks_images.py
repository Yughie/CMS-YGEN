import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="basecontent",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name="ContentBlock",
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
                    "block_type",
                    models.CharField(
                        choices=[
                            ("rich_text", "Rich Text"),
                            ("hero", "Hero"),
                            ("gallery", "Gallery"),
                            ("cta", "Call To Action"),
                        ],
                        max_length=32,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255)),
                ("body", models.TextField(blank=True)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("position", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocks",
                        to="cms.basecontent",
                    ),
                ),
            ],
            options={
                "ordering": ["content_id", "position", "id"],
            },
        ),
        migrations.CreateModel(
            name="ContentImage",
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
                    "image",
                    models.ImageField(upload_to="cms/images/%Y/%m/%d"),
                ),
                ("alt_text", models.CharField(max_length=255)),
                ("caption", models.CharField(blank=True, max_length=500)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_primary", models.BooleanField(default=False)),
                (
                    "content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="cms.basecontent",
                    ),
                ),
            ],
            options={
                "ordering": ["content_id", "sort_order", "id"],
            },
        ),
        migrations.AddConstraint(
            model_name="contentblock",
            constraint=models.UniqueConstraint(
                fields=("content", "position"),
                name="cms_contentblock_unique_position_per_content",
            ),
        ),
        migrations.AddConstraint(
            model_name="contentimage",
            constraint=models.UniqueConstraint(
                condition=models.Q(is_primary=True),
                fields=("content",),
                name="cms_contentimage_single_primary_per_content",
            ),
        ),
        migrations.AddIndex(
            model_name="contentblock",
            index=models.Index(
                fields=["content", "position"],
                name="cms_content_content_4ea77f_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="contentblock",
            index=models.Index(
                fields=["content", "is_active"],
                name="cms_content_content_269c68_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="contentimage",
            index=models.Index(
                fields=["content", "sort_order"],
                name="cms_content_content_5d7b5f_idx",
            ),
        ),
    ]

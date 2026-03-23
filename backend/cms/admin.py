from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.db import models

from cms.models import (
	BaseContent,
	ContentBlock,
	ContentImage,
	ContentMetaItem,
	ProductDetails,
	RealEstateDetails,
)


class ContentBlockInline(admin.StackedInline):
	model = ContentBlock
	extra = 0
	fields = (
		"position",
		"block_type",
		"title",
		"body",
		"cta_label",
		"cta_href",
		"cta_style",
		"cta_target",
		"payload",
		"is_active",
	)
	ordering = ("position", "id")
	show_change_link = True
	formfield_overrides = {
		models.JSONField: {
			"widget": AdminTextareaWidget(
				attrs={
					"rows": 4,
					"style": "font-family:Consolas,monospace;",
				}
			)
		},
	}

	def get_formset(self, request, obj=None, **kwargs):
		formset = super().get_formset(request, obj, **kwargs)
		payload_field = formset.form.base_fields.get("payload")
		if payload_field:
			payload_field.help_text = (
				"Optional advanced config as JSON object. "
				"For CTA, prefer the dedicated CTA fields above."
			)
		return formset


class ContentMetaItemInline(admin.TabularInline):
	model = ContentMetaItem
	extra = 0
	fields = ("key", "value")
	ordering = ("key",)
	show_change_link = False


class ContentImageInline(admin.StackedInline):
	model = ContentImage
	extra = 0
	fields = ("sort_order", "is_primary", "alt_text", "caption", "image")
	ordering = ("sort_order", "id")
	show_change_link = True


@admin.register(BaseContent)
class BaseContentAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"title",
		"description",
		"industry",
		"status",
		"publish_at",
		"updated_at",
	)
	list_filter = ("industry", "status")
	search_fields = ("title", "slug", "seo_title")
	readonly_fields = ("created_at", "updated_at")
	inlines = (ContentMetaItemInline, ContentBlockInline, ContentImageInline)
	formfield_overrides = {
		models.JSONField: {
			"widget": AdminTextareaWidget(
				attrs={
					"rows": 4,
					"style": "font-family:Consolas,monospace;",
				}
			)
		},
	}


@admin.register(RealEstateDetails)
class RealEstateDetailsAdmin(admin.ModelAdmin):
	list_display = ("id", "content", "listing_price", "currency", "address_line")
	search_fields = ("content__slug", "address_line")


@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
	list_display = ("id", "content", "sku", "price", "stock_quantity")
	search_fields = ("sku", "content__slug")


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
	list_display = ("id", "content", "block_type", "position", "is_active")
	list_filter = ("block_type", "is_active")
	search_fields = ("content__slug", "title")
	fields = (
		"content",
		"block_type",
		"title",
		"body",
		"cta_label",
		"cta_href",
		"cta_style",
		"cta_target",
		"payload",
		"position",
		"is_active",
	)
	formfield_overrides = {
		models.JSONField: {
			"widget": AdminTextareaWidget(
				attrs={
					"rows": 6,
					"style": "font-family:Consolas,monospace;",
				}
			)
		},
	}


@admin.register(ContentImage)
class ContentImageAdmin(admin.ModelAdmin):
	list_display = ("id", "content", "sort_order", "is_primary", "alt_text")
	list_filter = ("is_primary",)
	search_fields = ("content__slug", "alt_text")


@admin.register(ContentMetaItem)
class ContentMetaItemAdmin(admin.ModelAdmin):
	list_display = ("id", "content", "key", "value")
	search_fields = ("content__slug", "key", "value")

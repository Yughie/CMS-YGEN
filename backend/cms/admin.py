from django.contrib import admin

from cms.models import (
	BaseContent,
	ContentBlock,
	ContentImage,
	ProductDetails,
	RealEstateDetails,
)


class ContentBlockInline(admin.TabularInline):
	model = ContentBlock
	extra = 0
	fields = ("position", "block_type", "title", "is_active")
	ordering = ("position", "id")


class ContentImageInline(admin.TabularInline):
	model = ContentImage
	extra = 0
	fields = ("sort_order", "is_primary", "alt_text", "caption", "image")
	ordering = ("sort_order", "id")


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
	inlines = (ContentBlockInline, ContentImageInline)


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


@admin.register(ContentImage)
class ContentImageAdmin(admin.ModelAdmin):
	list_display = ("id", "content", "sort_order", "is_primary", "alt_text")
	list_filter = ("is_primary",)
	search_fields = ("content__slug", "alt_text")

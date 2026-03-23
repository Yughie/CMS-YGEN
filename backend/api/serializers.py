from rest_framework import serializers

from cms.models import (
    BaseContent,
    ContentBlock,
    ContentImage,
    ContentMetaItem,
    ProductDetails,
    RealEstateDetails,
)


class ContentMetaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentMetaItem
        fields = ["key", "value"]


class ContentBlockSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()

    def get_payload(self, obj: ContentBlock) -> dict:
        return obj.resolved_payload()

    class Meta:
        model = ContentBlock
        fields = [
            "id",
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
        ]


class ContentImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ContentImage
        fields = [
            "id",
            "image_url",
            "alt_text",
            "caption",
            "sort_order",
            "is_primary",
        ]

    def get_image_url(self, obj: ContentImage) -> str:
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class RealEstateDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateDetails
        fields = [
            "listing_price",
            "currency",
            "bedrooms",
            "bathrooms",
            "area_sqft",
            "address_line",
        ]


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        fields = ["sku", "price", "stock_quantity"]


class BaseContentSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", allow_null=True)
    metadata = serializers.SerializerMethodField()
    meta_items = ContentMetaItemSerializer(many=True, read_only=True)
    blocks = ContentBlockSerializer(many=True, read_only=True)
    images = ContentImageSerializer(many=True, read_only=True)
    real_estate_details = RealEstateDetailsSerializer(read_only=True)
    product_details = ProductDetailsSerializer(read_only=True)

    def get_metadata(self, obj: BaseContent) -> dict:
        combined = dict(obj.metadata or {})
        for item in obj.meta_items.all():
            combined[item.key] = item.value
        return combined

    class Meta:
        model = BaseContent
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "industry",
            "status",
            "publish_at",
            "unpublish_at",
            "owner_id",
            "metadata",
            "meta_items",
            "blocks",
            "images",
            "real_estate_details",
            "product_details",
            "updated_at",
        ]
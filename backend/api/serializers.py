from rest_framework import serializers

from cms.models import BaseContent, ContentBlock, ContentImage


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = [
            "id",
            "block_type",
            "title",
            "body",
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


class BaseContentSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", allow_null=True)
    blocks = ContentBlockSerializer(many=True, read_only=True)
    images = ContentImageSerializer(many=True, read_only=True)

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
            "blocks",
            "images",
            "updated_at",
        ]
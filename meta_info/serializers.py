"""Books app serializers."""

from rest_framework import serializers

from meta_info.models import (
    Tag,
    MetaInfo,
)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        read_only_fields = (
            'id',
            'created_at',
        )
        fields = read_only_fields + (
            'slug',
            'copy',
        )


class MetaSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = MetaInfo
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
        )
        fields = read_only_fields + (
            'copy',
            'json',
            'tags',
        )
        exclude = []
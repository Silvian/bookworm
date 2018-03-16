"""Books app serializers."""

from rest_framework import serializers

from meta_info.models import (
    Tag,
    Meta,
)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'slug',
            'copy',
        )
        exclude = []


class MetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meta
        fields = (
            'id',
            'copy',
            'json',
            'tags',
        )
        exclude = []

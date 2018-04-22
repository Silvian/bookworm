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
            'slug',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'copy',
            'tags',
        )


class MetaSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = MetaInfo
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'copy',
            'json',
            'tags',
        )
        exclude = ()

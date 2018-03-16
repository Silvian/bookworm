"""Books app serializers."""

from rest_framework import serializers

from profile.models import (
    Profile,
    ContactMethod,
)


class ContactMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMethod
        fields = (
            'id',
            'detail',
            'email',
            'json',
        )
        exclude = []


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'name_title',
            'name_first',
            'name_family',
            'name_middle',
            'birth_date',
        )
        exclude = []

"""Books app feature tests."""

import factory
from django_common.auth_backends import User

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice
from rest_framework import status
from rest_framework.test import APITestCase


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    username = factory.Faker('name')

    class Meta:
        model = User

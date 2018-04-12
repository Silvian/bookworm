from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """Ensure the user assigned to a model can only access that model."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

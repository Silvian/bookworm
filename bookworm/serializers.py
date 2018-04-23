
from bookworm.exceptions import OperationReservedInternally


class ProfileAssociationSerializerMixin:
    """Manage the creation of an object with reference to a Profile."""

    def validate(self, data):
        """Validate for profile assignment to validated_data"""
        current_user = self.context['request'].user
        if 'profile' not in data:
            data['profile'] = current_user.profile
        elif current_user.id != data['profile']:
            if not current_user.is_superuser and not current_user.is_staff:
                raise OperationReservedInternally(current_user)
        return super().validate(data)

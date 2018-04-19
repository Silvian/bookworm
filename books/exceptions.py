from rest_framework.serializers import ValidationError


class OperationReservedInternally(ValidationError):

    def __init__(self, current_user):
        super().__init__([{
            'code': 'unexpected_user',
            'message': '{}, get realz!'.format(
                current_user.profile.display_name
            ),
        }])

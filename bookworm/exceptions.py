from rest_framework.serializers import ValidationError


class OperationReservedInternally(ValidationError):

    def __init__(self, current_user):
        super().__init__([{
            'code': 'unexpected_user',
            'message': '{}, get realz!'.format(
                current_user.profile.display_name
            ),
        }])


class PublishableObjectNotDefined(ValidationError):

    def __init__(self, attempted_instance, action='publish'):
        super().__init__([{
            'code': 'publishable_class_undefined',
            'message': '{} {} attempt without `Publishable` info.'.format(
                attempted_instance.__class__,
                action,
            ),
        }])

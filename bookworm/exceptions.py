import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class OperationReservedInternally(ValidationError):

    def __init__(self, current_user):
        super().__init__([{
            'code': 'unexpected_user',
            'message': '{}, get realz!'.format(
                current_user.profile.display_name
            ),
        }])
        logger.error(self)


class InvalidOperation(ValidationError):

    def __init__(self, obj):
        super().__init__([{
            'code': 'invalid_operation',
            'message': '{}, nopez!'.format(
                obj
            ),
        }])
        logger.error(self)


class PublishableObjectNotDefined(ValidationError):

    def __init__(self, attempted_instance, action='publish'):
        super().__init__([{
            'code': 'publishable_class_undefined',
            'message': '{} {} attempt without `Publishable` info.'.format(
                attempted_instance.__class__,
                action,
            ),
        }])
        logger.error(self)


class PublishableValidationError(ValidationError):

    def __init__(self, attempted_instance, errors):
        super().__init__([{
            'code': 'publishable_class_undefined',
            'message': '{} invalid publish attempt.'.format(
                attempted_instance.__class__,
            ),
            'errors': errors,
        }])
        logger.error(self)

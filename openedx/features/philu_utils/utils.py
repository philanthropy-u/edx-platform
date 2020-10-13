"""
Utility methods related to PhilU
"""
from logging import getLogger

from django.core.validators import ValidationError
from django.utils.translation import ugettext as _

log = getLogger(__name__)


def validate_file_size(_file, max_allowed_size):
    """
    Validate maximum allowed file size to upload

    Arguments:
        _file (File): file that needs to be validated
        max_allowed_size (int): maximum allowed file size in bytes

    Raises:
        ValidationError: If file size exceeds
    """
    size = getattr(_file, 'size', None)

    if not max_allowed_size:
        raise Exception(
            _('Max allowed size must be specified')
        )

    if size and max_allowed_size < size:
        raise ValidationError(
            _('File size must not exceed {size} MB').format(size=max_allowed_size / 1024 / 1024)
        )


def bytes_to_mb(bytes_):
    """
    Convert size from bytes to MB

    Arguments:
        bytes_ (int): size in bytes

    Returns:
        int: size in MB
    """
    return bytes_ / 1024 / 1024


def get_anonymous_user(user, course_id):
    try:
        from student.models import AnonymousUserId
        return AnonymousUserId.objects.get(user=user, course_id=course_id)
    except AnonymousUserId.DoesNotExist:
        log.info('Anonymous Id does not exist for User: {user} & Course: {course}'.format(user=user, course=course_id))
    except AnonymousUserId.MultipleObjectsReturned:
        log.info('Multiple Anonymous Ids for User: {user} & Course: {course}'.format(user=user, course=course_id))

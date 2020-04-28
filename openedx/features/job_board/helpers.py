import os
from uuid import uuid4

from django.core.validators import ValidationError
from django.utils.translation import ugettext as _

from openedx.features.job_board.constants import LOGO_IMAGE_MAX_SIZE
from django.utils.deconstruct import deconstructible


def validate_file_size(file):
    """
    Validate maximum allowed file upload size, raise validation error if file size exceeds.
    :param file: file that needs to be validated for size
    """
    size = getattr(file, 'size', None)
    if size and LOGO_IMAGE_MAX_SIZE < size:
        raise ValidationError(
            _('File size must not exceed {size} MB').format(size=LOGO_IMAGE_MAX_SIZE / 1024 / 1024)
        )


@deconstructible
class UploadToPathAndRename(object):
    """
    Rename file uploaded by user.
    """

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        file_extension = filename.split('.')[-1] if filename else ''
        # get filename
        if instance.pk:
            filename = 'logo_{}.{}'.format(instance.pk, file_extension)
        else:
            # set filename as random string
            filename = 'logo_{}.{}'.format(uuid4().hex, file_extension)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)

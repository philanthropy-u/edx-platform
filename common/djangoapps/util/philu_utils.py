import os
from uuid import uuid4

from django.db.models import ImageField
from django.utils.deconstruct import deconstructible


def extract_utm_params(input_dict):
    """
    This method returns a subset of the input dictionary that only contains the utm params found
    in the input_dict
    :param input_dict: a dictionary that may or may not contain utm parameters
    :return: a dictionary containing only utm_params found in the utm_keys
    """
    if not input_dict:
        return dict()

    utm_keys = [
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_content',
        'utm_term'
    ]

    return {key: value for key, value in input_dict.items() if key in utm_keys}


@deconstructible
class UploadToPathAndRename(object):
    """
    Rename file uploaded by user.
    """

    def __init__(self, path, field_name):
        self.sub_path = path
        self.field_name = field_name

    def __call__(self, instance, filename):
        file_extension = filename.split('.')[-1] if filename else ''

        name_prefix = 'image' if instance._meta.get_field(self.field_name).__class__ is ImageField else 'file'

        # if pk has been created then use pk otherwise set filename as random string
        unique_name = instance.pk or uuid4().hex
        filename = '{}_{}.{}'.format(name_prefix, unique_name, file_extension)

        # return the whole path to the file
        return os.path.join(self.sub_path, filename)

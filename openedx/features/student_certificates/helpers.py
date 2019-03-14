import boto
from boto.s3.key import Key
from django.conf import settings


CERTIFICATE_IMG_PREFIX = 'certificates_images'


def upload_to_s3(file_path, s3_bucket, key_name):
    """
    :param file_path: path of the file we have to upload on s3
    :param s3_bucket: bucket in which we have to upload
    :param key_name: key by which we will place this file in the bucket
    :return:
    """
    aws_access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    conn = boto.connect_s3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    bucket = conn.get_bucket(s3_bucket)
    key = Key(bucket=bucket, name=key_name)
    key.set_contents_from_filename(file_path)


def get_certificate_image_url(certificate):
    """
    :param certificate:
    :return: return s3 url of corresponding image of the certificate
    """
    return 'https://s3.amazonaws.com/{bucket}/{prefix}/{uuid}.jpg'.format(
        bucket=getattr(settings, "FILE_UPLOAD_STORAGE_BUCKET_NAME", None),
        prefix=CERTIFICATE_IMG_PREFIX,
        uuid=certificate.verify_uuid
    )


def get_certificate_url(certificate):
    """
    :param certificate:
    :return: url of the certificate
    """
    return '{root_url}/certificates/{uuid}'.format(root_url=settings.LMS_ROOT_URL, uuid=certificate.verify_uuid)


def get_certificate_image_name(certificate):
    """
    :param certificate:
    :return: image name of the certificate
    """
    return '{uuid}.jpg'.format(uuid=certificate.verify_uuid)


def get_certificate_img_key(img_name):
    """
    :param img_name:
    :return: return S3 key name for the image name
    """
    return '{prefix}/{img_name}'.format(prefix=CERTIFICATE_IMG_PREFIX, img_name=img_name)

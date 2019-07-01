from __future__ import unicode_literals

import mock
from certificates.tests.factories import GeneratedCertificateFactory
from django.core.management import call_command
from django.db.models.signals import post_save
from factory.django import mute_signals
from lms.djangoapps.onboarding.tests.factories import UserFactory
from student.tests.factories import CourseEnrollmentFactory
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory


class CreateCertificateImage(SharedModuleStoreTestCase):
    """
        Tests for `create_certificates_image` command.
    """

    @mute_signals(post_save)
    def setUp(self):
        super(CreateCertificateImage, self).setUp()
        self.user = UserFactory()
        self.course = CourseFactory()
        self.course.certificates_display_behavior = "early_with_info"

    @mock.patch('openedx.features.student_certificates.tasks.task_create_certificate_img_and_upload_to_s3.delay')
    def test_command(self, mock_func):
        certificate_uuid = self._create_certificate('honor')
        call_command('create_certificates_image')
        mock_func.assert_called_once_with(verify_uuid=certificate_uuid)

    @mock.patch('openedx.features.student_certificates.tasks.task_create_certificate_img_and_upload_to_s3.delay')
    def test_command_with_date_argument(self, mock_func):
        certificate_uuid = self._create_certificate('honor')
        call_command('create_certificates_image', '--after=30/6/2019')
        mock_func.assert_called_once_with(verify_uuid=certificate_uuid)

    @mock.patch('openedx.features.student_certificates.tasks.task_create_certificate_img_and_upload_to_s3.delay')
    def test_command_with_uuid_argument(self, mock_func):
        certificate_uuid = self._create_certificate('honor')
        call_command('create_certificates_image', '--uuid={}'.format(certificate_uuid))
        mock_func.assert_called_once_with(verify_uuid=certificate_uuid)

    def _create_certificate(self, enrollment_mode):
        """Simulate that the user has a generated certificate. """
        CourseEnrollmentFactory.create(user=self.user, course_id=self.course.id, mode=enrollment_mode)
        certificate = GeneratedCertificateFactory(
            user=self.user,
            course_id=self.course.id,
            mode=enrollment_mode,
            status="downloadable",
            grade=0.98,
        )
        return certificate.verify_uuid

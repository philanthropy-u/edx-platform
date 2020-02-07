from mock import patch

from django.test import RequestFactory, TestCase

from student.tests.factories import RegistrationFactory, UserFactory

from openedx.features.student_account.helpers import compose_and_send_activation_email_custom


class ComposeAndSendActivationEmailTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().post('/user_api/v1/account/registration/')
        self.user = UserFactory.create()
        self.registration = RegistrationFactory.create(user=self.user)

    @patch('openedx.features.student_account.helpers.task_send_account_activation_email.delay')
    def test_compose_and_send_email_custom_normal(self, mocked_email_task):

        email_data = {
            "activation_link": 'http://edx.org/activate/{}'.format(self.registration.activation_key),
            "user_email": self.user.email,
            'first_name': self.user.first_name,
        }

        compose_and_send_activation_email_custom(self.request, self.registration, self.user)
        mocked_email_task.assert_called_once_with(email_data)




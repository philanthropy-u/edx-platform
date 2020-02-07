from mock import patch

from django.test import RequestFactory, TestCase

from student.tests.factories import RegistrationFactory, UserFactory

from openedx.features.student_account.helpers import compose_and_send_activation_email_custom


class ComposeAndSendActivationEmailTests(TestCase):
    """
    The purpose of this test is to check that the data being passed to the
    compose_and_send_activation_email_custom method stays the same.

    For this, we create a request, user, and registration type objects to
    generate the data just as the helper is supposed to and assert that
    it is the same
    """

    def setUp(self):
        """
        Create a new POST request using the RequestFactory, a user object
        using the UserFactory and a registration object using RegistrationFactory
        for each test case
        """

        self.request = RequestFactory().post('/user_api/v1/account/registration/')
        self.user = UserFactory.create()
        self.registration = RegistrationFactory.create(user=self.user)

    @patch('openedx.features.student_account.helpers.task_send_account_activation_email.delay')
    def test_compose_and_send_email_custom_normal(self, mocked_email_task):
        """
        Generate the data using the objects created in setUp, and assert that the
        activation email method is called only once and the data passed to it is
        the same as we expect
        """

        email_data = {
            'activation_link': 'http://edx.org/activate/{}'.format(self.registration.activation_key),
            'user_email': self.user.email,
            'first_name': self.user.first_name,
        }

        compose_and_send_activation_email_custom(self.request, self.registration, self.user)
        mocked_email_task.assert_called_once_with(email_data)




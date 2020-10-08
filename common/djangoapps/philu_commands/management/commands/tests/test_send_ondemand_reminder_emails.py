"""
Tests for 'send_ondemand_reminder_emails' command
"""
from datetime import datetime, timedelta

import mock
from ddt import ddt, file_data
from django.conf import settings
from django.core.management import call_command
from pytz import utc

from common.djangoapps.philu_commands.management.commands.send_ondemand_reminder_emails import (
    DAYS_FOR_EACH_MODULE,
    INACTIVITY_REMINDER_DAYS,
    ORA_ASSESSMENT_BLOCK,
    check_for_last_module_submission,
    get_all_ora_blocks,
    get_graded_ora_count,
    get_last_module_ora,
    get_suggested_course_deadline,
    has_inactivity_threshold_reached,
    send_reminder_email
)
from common.lib.mandrill_client.client import MandrillClient
from lms.djangoapps.onboarding.tests.factories import UserFactory
from openedx.core.djangoapps.content.course_overviews.tests.factories import CourseOverviewFactory
from openedx.features.assessment.tests.factories import SubmissionFactory
from student.tests.factories import AnonymousUserIdFactory, CourseEnrollmentFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory


@ddt
class TestSendOnDemandReminderEmails(ModuleStoreTestCase):
    """
    Class contains tests for 'send_ondemand_reminder_emails' command
    """

    def setUp(self):
        super(TestSendOnDemandReminderEmails, self).setUp()
        self.user = UserFactory()
        self.course = CourseFactory.create(display_name='test course 1', run='Testing_course_1')
        start_date = datetime.strptime('2020-02-20', '%Y-%m-%d')
        end_date = datetime.strptime('2021-02-20', '%Y-%m-%d')
        self.course_overview = CourseOverviewFactory.create(
            id=self.course.id, start=start_date, end=end_date, self_paced=True)

    def test_has_inactivity_threshold_reached(self):
        """
        Test inactivity threshold by comparing 2 dates if their difference is equals to 10 days or not.
        """
        second_date = datetime.now(utc)

        date_at_ten_days_before_today = second_date - timedelta(days=INACTIVITY_REMINDER_DAYS)
        self.assertTrue(has_inactivity_threshold_reached(date_at_ten_days_before_today, second_date))

        date_at_seven_days_before_today = second_date - timedelta(days=7)
        self.assertFalse(has_inactivity_threshold_reached(date_at_seven_days_before_today, second_date))

    def test_get_suggested_course_deadline(self):
        """
        Test suggested course deadline.
        """
        enrollment_date = datetime.now(utc)
        chapters_list = [1, 2, 3, 4, 5]

        expected_result = enrollment_date + timedelta(days=(5 * DAYS_FOR_EACH_MODULE))
        self.assertEqual(expected_result, get_suggested_course_deadline(enrollment_date, chapters_list))

    def test_get_graded_ora_count(self):
        """
        Test graded ora count in a course.
        """
        ora_blocks = [
            self._get_dummy_ora_block(True),
            self._get_dummy_ora_block(False),
            self._get_dummy_ora_block(True)
        ]

        expected_result = 2
        self.assertEqual(expected_result, get_graded_ora_count(ora_blocks))

    def test_get_all_ora_blocks(self):
        """
        Test to get all ora blocks from a course.
        """
        all_blocks = {
            "blocks": {
                "block_id_1": self._get_dummy_ora_block(True),
                "block_id_2": {
                    "block_type": "chapter",
                    "graded": False,
                    "display_name": "chapter_1"
                },
                "block_id_3": self._get_dummy_ora_block(False)
            }
        }

        expected_result_length = 2
        self.assertEqual(expected_result_length, len(get_all_ora_blocks(all_blocks)))

    def test_check_for_last_module_submission(self):
        """
        Test if all the last modules ORAs are submitted or not.
        """
        last_module_ora = ["ora_id_1", "ora_id-2"]
        anonymous_user = AnonymousUserIdFactory()

        SubmissionFactory(student_item__student_id=anonymous_user.anonymous_user_id, student_item__item_id=last_module_ora[0])
        self.assertFalse(check_for_last_module_submission(last_module_ora, anonymous_user))

        SubmissionFactory(student_item__student_id=anonymous_user.anonymous_user_id, student_item__item_id=last_module_ora[1])
        self.assertTrue(check_for_last_module_submission(last_module_ora, anonymous_user))

    @file_data('data/test_data_for_send_ondemand_reminder_emails_test.json')
    def test_get_last_module_ora(self, reminder_emails_test_data):
        """
        Test if all the last modules ORAs are submitted or not.
        """
        reminder_emails_test_data = reminder_emails_test_data[0]['blocks']

        actual_result = get_last_module_ora(reminder_emails_test_data)

        if {'block_id_3', 'block_id_5'} <= reminder_emails_test_data.viewkeys() and \
            reminder_emails_test_data['block_id_3']['graded'] and \
            reminder_emails_test_data['block_id_5']['block_type'] == ORA_ASSESSMENT_BLOCK:
            self.assertEqual(['block_id_5'], actual_result)
        else:
            self.assertEqual(len(actual_result), 0)

    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_nth_chapter_link')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.MandrillClient.send_mail')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_my_account_link')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.log.info')
    def test_send_reminder_email(
        self,
        mock_log_info,
        mock_get_account_link,
        mock_send_email,
        mock_get_nth_chapter_link
    ):
        """
        Test send reminder emails with required context.
        """
        mock_get_nth_chapter_link.return_value = '{base_url}/courses/{course_id}/courseware/chapter_id/sequence_id/'\
            .format(base_url=settings.LMS_ROOT_URL, course_id=str(self.course.id))
        mock_get_account_link.return_value = 'www.some_testing_url.com/user/account'

        course_deadline = datetime.now(utc) + timedelta(days=30)

        send_reminder_email(self.user, self.course, course_deadline)

        expected_context = {
            'first_name': self.user.first_name,
            'course_name': self.course.display_name,
            'deadline_date': str(course_deadline),
            'course_url': mock_get_nth_chapter_link.return_value,
            'email_address': self.user.email,
            'unsubscribe_link': mock_get_account_link.return_value
        }

        mock_send_email.assert_called_once_with(
            MandrillClient.ON_DEMAND_REMINDER_EMAIL_TEMPLATE, self.user.email, expected_context
        )
        mock_log_info.assert_called_once_with("Emailing to %s Task Completed for course reminder", self.user.email)

    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.generate_course_structure')
    def test_send_ondemand_reminder_emails_command_with_no_active_course(self, mock_generate_course_structure):
        """
        Test send_ondemand_reminder_emails command with no active courses.
        """
        self.course_overview.end = datetime.strptime('2020-08-20', '%Y-%m-%d')
        self.course_overview.save()
        call_command('send_ondemand_reminder_emails')
        assert not mock_generate_course_structure.called

    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.log.error')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_all_ora_blocks')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.generate_course_structure')
    def test_send_ondemand_reminder_emails_command_with_invalid_course_structure(
        self, mock_generate_course_structure, mock_get_all_ora_bloacks, mock_log_message
    ):
        """
        Test send_ondemand_reminder_emails command with invalid course structure.
        """
        mock_generate_course_structure.return_value = {
            'structure': {}
        }
        call_command('send_ondemand_reminder_emails')

        assert mock_log_message.called
        assert not mock_get_all_ora_bloacks.called

    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.log.error')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_graded_ora_count')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_all_ora_blocks')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.generate_course_structure')
    def test_send_ondemand_reminder_emails_command_with_valid_course_structure_but_no_ora_blocks(
        self, mock_generate_course_structure, mock_get_all_ora_bloacks, mock_get_graded_ora_blocks, mock_log_message
    ):
        """
        Test send_ondemand_reminder_emails command with valid course structure but without content(blocks).
        """
        mock_generate_course_structure.return_value = self._get_dummy_course_structure()
        mock_get_all_ora_bloacks.return_value = []

        call_command('send_ondemand_reminder_emails')

        assert not mock_log_message.called
        assert not mock_get_graded_ora_blocks.called

    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_email_pref_on_demand_course')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_user_anonymous_id')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_last_module_ora')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_graded_ora_count')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_all_ora_blocks')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.generate_course_structure')
    def test_send_ondemand_reminder_emails_command_with_and_without_enrollments(
        self,
        mock_generate_course_structure,
        mock_get_all_ora_bloacks,
        mock_get_graded_ora_blocks,
        mock_get_last_module_ora,
        mock_get_user_anonymous_id,
        mock_get_email_pref_on_demand_course
    ):
        """
        Test send_ondemand_reminder_emails command with and without enrollments.
        """
        ora_dict = self._get_dummy_ora_block(True)
        mock_generate_course_structure.return_value = self._get_dummy_course_structure()
        mock_generate_course_structure.return_value['structure']['blocks']['block_id_4'] = ora_dict

        mock_get_all_ora_bloacks.return_value = [ora_dict]
        mock_get_last_module_ora.return_value = mock.ANY
        mock_get_graded_ora_blocks.return_value = mock.ANY
        mock_get_email_pref_on_demand_course.return_value = False

        call_command('send_ondemand_reminder_emails')
        assert not mock_get_user_anonymous_id.called
        assert not mock_get_email_pref_on_demand_course.called

        CourseEnrollmentFactory.create(user=self.user, course_id=self.course.id)
        call_command('send_ondemand_reminder_emails')
        mock_get_user_anonymous_id.assert_called_once_with(self.user, self.course.id)
        assert mock_get_email_pref_on_demand_course.called

# TODO: This is a very big test, it should be avoided by broken down command code into helpers and test them separately.

    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.send_reminder_email')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.has_inactivity_threshold_reached')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.log.info')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.check_for_last_module_submission')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_suggested_course_deadline')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.modulestore')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_email_pref_on_demand_course')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_user_anonymous_id')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_last_module_ora')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_graded_ora_count')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.get_all_ora_blocks')
    @mock.patch('philu_commands.management.commands.send_ondemand_reminder_emails.generate_course_structure')
    def test_send_ondemand_reminder_emails_command_with_and_without_last_module_ora_submission(
        self,
        mock_generate_course_structure,
        mock_get_all_ora_bloacks,
        mock_get_graded_ora_count,
        mock_get_last_module_ora,
        mock_get_user_anonymous_id,
        mock_get_email_pref_on_demand_course,
        mock_modulestore,
        mock_get_suggested_course_deadline,
        mock_check_for_last_module_submission,
        mock_log_message,
        mock_has_inactivity_threshold_reached,
        mock_send_reminder_email
    ):
        """
        Test send_ondemand_reminder_emails command with or without last module ORAs submissions.
        """
        ora_dict = self._get_dummy_ora_block(True)
        course_deadline = datetime.now(utc) + timedelta(days=30)

        enrollment = CourseEnrollmentFactory.create(user=self.user, course_id=self.course.id)
        anonymous_user = AnonymousUserIdFactory()

        mock_generate_course_structure.return_value = self._get_dummy_course_structure()
        mock_generate_course_structure.return_value['structure']['blocks']['block_id_4'] = ora_dict

        mock_get_suggested_course_deadline.return_value = course_deadline
        mock_get_all_ora_bloacks.return_value = [ora_dict]
        mock_get_last_module_ora.return_value = [ora_dict]
        mock_get_graded_ora_count.return_value = 1
        mock_get_user_anonymous_id.return_value = anonymous_user
        mock_check_for_last_module_submission.return_value = False
        mock_has_inactivity_threshold_reached.return_value = True

        call_command('send_ondemand_reminder_emails')
        assert not mock_log_message.called
        mock_has_inactivity_threshold_reached.assert_called_once_with(enrollment.created.date(), datetime.now().date())
        mock_send_reminder_email.assert_called_once_with(self.user, self.course_overview, course_deadline)

        ora_1_submission = SubmissionFactory(student_item__student_id=anonymous_user.anonymous_user_id,
                                             student_item__course_id=self.course.id)
        mock_has_inactivity_threshold_reached.reset_mock()
        mock_check_for_last_module_submission.return_value = True

        call_command('send_ondemand_reminder_emails')
        mock_log_message.assert_called_once_with('Last module Graded ORAs submitted so no further check')
        assert not mock_has_inactivity_threshold_reached.called

        # Check if email had been sent to user in past or not (Email sent in past)
        # Update enrollment $ submission date
        enrollment.created = datetime.now(utc) - timedelta(days=20)
        enrollment.save()
        ora_1_submission.created_at = datetime.now(utc) - timedelta(days=10)
        ora_1_submission.save()

        # Add new Ora block in mock_generate_course_structure
        mock_generate_course_structure.return_value['structure']['blocks']['block_id_5'] = ora_dict
        # mock_generate_course_structure.return_value['structure']['blocks']['block_id_6'] = ora_dict

        # ora_2_submission = SubmissionFactory(student_item__student_id=anonymous_user.anonymous_user_id,
        #                                      student_item__course_id=self.course.id)

        mock_get_all_ora_bloacks.return_value = [ora_dict, ora_dict]
        mock_get_last_module_ora.return_value = [ora_dict, ora_dict]
        mock_get_graded_ora_count.return_value = 2
        mock_check_for_last_module_submission.return_value = False

        mock_log_message.reset_mock()
        mock_has_inactivity_threshold_reached.reset_mock()
        call_command('send_ondemand_reminder_emails')
        # mock_log_message.assert_called_once_with('Inactivity threshold reached so check for previous ORAs')
        self.assertEqual(mock_log_message.call_count, 2)
        self.assertEqual(mock_has_inactivity_threshold_reached.call_count, 2)

        # Check if email had been sent to user in past or not (Email didn't sent in past)
        # Update enrollment date
        enrollment.created = datetime.now(utc) - timedelta(days=18)
        enrollment.save()

        mock_log_message.reset_mock()
        mock_send_reminder_email.reset_mock()
        mock_has_inactivity_threshold_reached.reset_mock()
        # mock_has_inactivity_threshold_reached.return_value = mock.ANY
        # mock_has_inactivity_threshold_reached.side_effect = [True, True, False]
        call_command('send_ondemand_reminder_emails')
        mock_log_message.assert_called_once_with('Inactivity threshold reached so check for previous ORAs')
        # self.assertEqual(mock_log_message.call_count, 2)
        self.assertEqual(mock_has_inactivity_threshold_reached.call_count, 1)
        mock_send_reminder_email.assert_called_once_with(self.user, self.course_overview, course_deadline)


    def _get_dummy_ora_block(self, is_graded):
        """
        This is to get dummy ora block
        Arguments:
            is_graded (bool): ORA created will be graded or not.
        Returns:
            dict: dictionary containing ora block
        """
        return {
            "block_type": ORA_ASSESSMENT_BLOCK,
            "graded": is_graded,
            "display_name": "ORA"
        }

    def _get_dummy_course_structure(self):
        """
        This is a data util to get dummy structure of course.
        Returns:
            dict: dictionary containing dummy structure.
        """
        return {
            'structure': {
                "blocks": {
                    "block_id_1": {
                        "block_type": "course",
                        "graded": False,
                        "display_name": "course name"
                    },
                    "block_id_2": {
                        "block_type": "chapter",
                        "graded": False,
                        "display_name": "chapter_1"
                    },
                    "block_id_3": {
                        "block_type": "sequential",
                        "graded": True,
                        "display_name": "sequential"
                    }
                }
            }
        }

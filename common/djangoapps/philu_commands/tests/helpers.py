"""
Tests philu_commands helpers
"""
from __future__ import unicode_literals

from datetime import datetime, timedelta

import pytz
from django.db.models import signals
from factory.django import mute_signals
from mock import Mock, patch

from philu_commands.helpers import generate_course_structure, has_active_certificate
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory


class MockModuleStoreTest(object):
    """
    Class to mock modulestore class functions, e.g. bulk_operations
    """
    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class TestHelpers(ModuleStoreTestCase):
    """
    Tests for `philu_commands helpers`
    """

    @mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        """
        This function is responsible for creating courses for every test and mocking the function for tests.
        """
        super(TestHelpers, self).setUp()
        self.course = CourseFactory.create(display_name='test course 1', run='Testing_course_1')
        self.course.end = datetime.now(pytz.UTC) - timedelta(hours=2)

    @patch('philu_commands.helpers.modulestore')
    def test_generate_course_structure(self, mock_modulestore):
        """
        Test 'Successfully generate course structure'
        """
        mock_response = Mock(name='mock module store', **{'bulk_operations.return_value': MockModuleStoreTest(),
                                                          'get_course.return_value': self.course})
        mock_modulestore.return_value = mock_response
        course_structure_data = generate_course_structure(self.course.id)
        expected_course_object = {
            'structure': {
                'blocks': {
                    u'i4x://org.0/course_0/course/Testing_course_1': {
                        'block_type': 'course', 'graded': False, 'format': None,
                        'usage_key': u'i4x://org.0/course_0/course/Testing_course_1',
                        'children': [], 'display_name': u'test course 1'}},
                'root': u'i4x://org.0/course_0/course/Testing_course_1'}, 'discussion_id_map': {}
        }
        assert course_structure_data == expected_course_object

    def test_has_active_certificate(self):
        """
        Test 'has active certificates'
        """
        does_not_have_cert = has_active_certificate(self.course)
        self.assertEqual(does_not_have_cert, False)
        certificates = {
            'id': 1,
            'name': 'Test Certificate',
            'description': 'Test Description',
            'course_title': 'course_title_Test',
            'org_logo_path': '/t4x/orgX/testX/asset/org-logo-{}.png',
            'version': 1,
            'is_active': True
        }
        self.course.certificates = {'certificates': [certificates]}
        has_certificate = has_active_certificate(self.course)
        self.assertEqual(has_certificate, True)

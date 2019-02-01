from django.contrib.auth.models import User
from django.test import TestCase

from ..views import get_course_cards
from ..models import CourseCard
from django.core.urlresolvers import reverse

from xmodule.modulestore.django import modulestore
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

from datetime import datetime, timedelta


class CourseCardBaseClass(ModuleStoreTestCase):
    def setUp(self):
        super(CourseCardBaseClass, self).setUp()

        self.user = User.objects.create_user('test_user', 'test_user+courses@edx.org', 'foo')
        self.admin = User.objects.create_user('Mark', 'admin+courses@edx.org', 'foo')
        self.admin.is_staff = True

        org = 'edX'
        course_number = 'CS101'
        course_run = '2015_Q1'
        display_name = 'test course'

        self.course = CourseFactory.create(org=org, number=course_number, run=course_run, display_name=display_name,
                                           default_store=ModuleStoreEnum.Type.split)
        CourseCard(course_id=self.course.id, course_name=display_name, is_enabled=True)


    def test_case_1(self):
        response = self.client.get('courses')
        self.assertFalse(False)
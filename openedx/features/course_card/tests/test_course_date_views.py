from datetime import datetime, timedelta

from custom_settings.models import CustomSettings

from pyquery import PyQuery as pq
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from openedx.core.djangoapps.theming.models import SiteTheme

from ..models import CourseCard
from .helpers import set_course_dates


class CourseCardBaseClass(ModuleStoreTestCase):

    def setUp(self):
        super(CourseCardBaseClass, self).setUp()

        org = 'edX'
        course_number_f = 'CS101'
        course_run = '2015_Q1'
        display_name_f = 'test course 1'

        self.course = CourseFactory.create(org=org, number=course_number_f, run=course_run,
                                           display_name=display_name_f,
                                           default_store=ModuleStoreEnum.Type.split,
                                           start=datetime.utcnow() - timedelta(days=30),
                                           end=datetime.utcnow() + timedelta(days=30))

        self.course.save()
        CourseCard(course_id=self.course.id, course_name=self.course.display_name, is_enabled=True).save()

    @classmethod
    def setUpClass(cls):
        super(CourseCardBaseClass, cls).setUpClass()
        site = Site(domain='testserver', name='test')
        site.save()
        theme = SiteTheme(site=site, theme_dir_name='philu')
        theme.save()


class CourseCardViewBaseClass(CourseCardBaseClass):

    def test_catalog_course_date(self):
        date_time_format = '%b %-d, %Y'
        set_course_dates(self.course, -30, -10, -5, 30)
        save_course_custom_settings(self.course.id)
        response = self.client.get(reverse('courses'))
        self.assertEqual(pq(response.content)("div.course-date > span")[2].text.strip(),
                         datetime.utcnow().strftime(date_time_format))

    def test_about_course_date(self):
        date_time_format = '%b %-d, %Y'
        set_course_dates(self.course, -30, -10, -5, 30)
        save_course_custom_settings(self.course.id)
        response = self.client.get(reverse('about_course', args=[self.course.id]))
        self.assertEqual(pq(response.content)("p.start-date")[0].text, datetime.utcnow().strftime(date_time_format))


def save_course_custom_settings(course_key_string):
    course_settings = CustomSettings(id=course_key_string, course_short_id=1, course_open_date=datetime.utcnow())
    course_settings.save()
    return course_settings

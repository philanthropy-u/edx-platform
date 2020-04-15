from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from openedx.core.djangoapps.theming.models import SiteTheme
from openedx.features.job_board.views import JobCreateView, JobListView
from openedx.features.job_board.tests.factories import JobFactory


class JobBoardViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(JobBoardViewTest, cls).setUpClass()
        site = Site(domain='testserver', name='test')
        site.save()
        theme = SiteTheme(site=site, theme_dir_name='philu')
        theme.save()

    def test_job_create_view(self):
        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(JobCreateView.fields, '__all__')

    def test_job_detail_view_invalid_pk(self):
        response = self.client.get(reverse('job_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_job_detail_view_valid_pk(self):
        job = JobFactory()
        job.save()
        response = self.client.get(reverse('job_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(JobListView.paginate_by, 10)
        self.assertEqual(JobListView.ordering, ['-created'])


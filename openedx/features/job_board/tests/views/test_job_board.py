from django.test import TestCase
from django.urls import reverse

from openedx.core.djangolib.testing.philu_utils import configure_philu_theme
from openedx.features.job_board.constants import (
    JOB_COMP_HOURLY_KEY,
    JOB_COMP_SALARIED_KEY,
    JOB_COMP_VOLUNTEER_KEY,
    JOB_HOURS_FREELANCE_KEY,
    JOB_HOURS_FULLTIME_KEY,
    JOB_HOURS_PARTTIME_KEY,
    JOB_PARAM_CITY_KEY,
    JOB_PARAM_COUNTRY_KEY,
    JOB_PARAM_QUERY_KEY,
    JOB_PARAM_TRUE_VALUE,
    JOB_TYPE_ONSITE_KEY,
    JOB_TYPE_REMOTE_KEY
)
from openedx.features.job_board.models import Job
from openedx.features.job_board.tests.factories import JobFactory
from openedx.features.job_board.views import JobCreateView, JobListView
from rest_framework import status


class JobBoardViewTest(TestCase):

    def setUp(self):
        self.page_length = 10
        self.number_of_jobs = 15
        self.client.logout()
        self.jobs = []
        for i in range(self.number_of_jobs):
            self.jobs.append(JobFactory())

    @classmethod
    def setUpClass(cls):
        super(JobBoardViewTest, cls).setUpClass()
        configure_philu_theme()

    def test_job_create_view(self):
        response = self.client.get(reverse('job_create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(JobCreateView.form_class.Meta.fields, '__all__')

    def test_create_view_post_successful(self):
        self.client.post('/jobs/create/', {"function": "dummy function",
                                           "city": "Lahore",
                                           "description": "dummy description",
                                           "title": "second title",
                                           "country": "AX",
                                           "company": "dummy company",
                                           "responsibilities": "dummy responsibilities",
                                           "hours": "parttime",
                                           "compensation": "salaried",
                                           "contact_email": "test@test.com",
                                           "logo": "",
                                           "type": "remote",
                                           "website_link": ""})
        self.assertEqual(Job.objects.all().count(), self.number_of_jobs + 1)

    def test_create_view_post_unsuccessful(self):
        self.client.post('/jobs/create/', {"function": "dummy function",
                                           "city": "Lahore",
                                           "description": "dummy description",
                                           "title": "second title",
                                           "country": "AX",
                                           "company": "dummy company",
                                           "responsibilities": "dummy responsibilities",
                                           "hours": "parttime",
                                           "compensation": "salaried",
                                           "contact_email": "test", #incorrect email
                                           "logo": "",
                                           "type": "remote",
                                           "website_link": ""})
        self.assertEqual(Job.objects.all().count(), self.number_of_jobs)

    def test_job_detail_view_invalid_pk(self):
        response = self.client.get(reverse('job_detail', kwargs={'pk': 1}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_detail_view_valid_pk(self):
        response = self.client.get(reverse('job_detail', kwargs={'pk': self.jobs[0].pk}), follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(JobListView.paginate_by, self.page_length)
        self.assertEqual(JobListView.ordering, ['-created'])

    def test_job_list_view_pagination(self):
        response_first_page = self.client.get(reverse('job_list'))
        self.assertEqual(response_first_page.status_code, status.HTTP_200_OK)
        self.assertTrue('is_paginated' in response_first_page.context_data)
        self.assertTrue(response_first_page.context_data['is_paginated'] is True)
        self.assertTrue(len(response_first_page.context_data['job_list']) == self.page_length)

        response_second_page = self.client.get(reverse('job_list') + '?page=2')
        self.assertEqual(response_second_page.status_code, status.HTTP_200_OK)
        self.assertTrue('is_paginated' in response_second_page.context_data)
        self.assertTrue(response_second_page.context_data['is_paginated'] is True)
        self.assertTrue(len(response_second_page.context_data['job_list']) == self.number_of_jobs-self.page_length)

    def test_job_list_view_filters_job_type(self):
        number_of_remote_jobs = 0
        number_of_onsite_jobs = 0

        for job in self.jobs:
            if job.type is JOB_TYPE_REMOTE_KEY:
                number_of_remote_jobs += 1
            if job.type is JOB_TYPE_ONSITE_KEY:
                number_of_onsite_jobs += 1

        response = self.client.get(reverse('job_list') + '?' + JOB_TYPE_REMOTE_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_TYPE_REMOTE_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_remote_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.type, JOB_TYPE_REMOTE_KEY)

        response = self.client.get(reverse('job_list') + '?' + JOB_TYPE_ONSITE_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_TYPE_ONSITE_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_onsite_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.type, JOB_TYPE_ONSITE_KEY)

    def test_job_list_view_filters_job_compensation(self):
        number_of_volunteer_jobs = 0
        number_of_hourly_jobs = 0
        number_of_salaried_jobs = 0

        for job in self.jobs:
            if job.compensation is JOB_COMP_VOLUNTEER_KEY:
                number_of_volunteer_jobs += 1
            if job.compensation is JOB_COMP_HOURLY_KEY:
                number_of_hourly_jobs += 1
            if job.compensation is JOB_COMP_SALARIED_KEY:
                number_of_salaried_jobs += 1

        response = self.client.get(reverse('job_list') + '?' + JOB_COMP_VOLUNTEER_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_COMP_VOLUNTEER_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_volunteer_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.compensation, JOB_COMP_VOLUNTEER_KEY)

        response = self.client.get(reverse('job_list') + '?' + JOB_COMP_HOURLY_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_COMP_HOURLY_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_hourly_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.compensation, JOB_COMP_HOURLY_KEY)

        response = self.client.get(reverse('job_list') + '?' + JOB_COMP_SALARIED_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_COMP_SALARIED_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_salaried_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.compensation, JOB_COMP_SALARIED_KEY)

    def test_job_list_view_filters_job_hours(self):
        number_of_fulltime_jobs = 0
        number_of_parttime_jobs = 0
        number_of_freelance_jobs = 0

        for job in self.jobs:
            if job.hours is JOB_HOURS_FULLTIME_KEY:
                number_of_fulltime_jobs += 1
            if job.hours is JOB_HOURS_PARTTIME_KEY:
                number_of_parttime_jobs += 1
            if job.hours is JOB_HOURS_FREELANCE_KEY:
                number_of_freelance_jobs += 1

        response = self.client.get(reverse('job_list') + '?' + JOB_HOURS_FULLTIME_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_HOURS_FULLTIME_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_fulltime_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.hours, JOB_HOURS_FULLTIME_KEY)

        response = self.client.get(reverse('job_list') + '?' + JOB_HOURS_PARTTIME_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_HOURS_PARTTIME_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_parttime_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.hours, JOB_HOURS_PARTTIME_KEY)

        response = self.client.get(reverse('job_list') + '?' + JOB_HOURS_FREELANCE_KEY + '=' + JOB_PARAM_TRUE_VALUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields'][JOB_HOURS_FREELANCE_KEY], JOB_PARAM_TRUE_VALUE)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == number_of_freelance_jobs)
        for job in response.context_data['job_list']:
            self.assertEqual(job.hours, JOB_HOURS_FREELANCE_KEY)

    def test_job_list_view_filters_job_location(self):
        job = JobFactory(country='PK', city='Karachi')
        response = self.client.get(reverse(
            'job_list') + '?' + JOB_PARAM_CITY_KEY + '=' + job.city + '&' + JOB_PARAM_COUNTRY_KEY + '=' + job.country.name)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields']['country'], job.country.name)
        self.assertTrue(response.context_data['search_fields']['city'], job.city)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == 1)
        self.assertTrue(response.context_data['job_list'][0].country.name == job.country.name)
        self.assertTrue(response.context_data['job_list'][0].city == job.city)

    def test_job_list_view_filters_job_query(self):
        job = JobFactory(title='custom_job')
        response = self.client.get(reverse('job_list') + '?' + JOB_PARAM_QUERY_KEY + '=' + job.title)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context_data['search_fields']['query'], job.title)
        self.assertTrue(response.context_data['filtered'], True)
        self.assertTrue(len(response.context_data['job_list']) == 1)
        self.assertTrue(job.title in response.context_data['job_list'][0].title)

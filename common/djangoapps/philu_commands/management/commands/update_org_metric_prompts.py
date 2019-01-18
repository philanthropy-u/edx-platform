from django.core.management.base import BaseCommand
from lms.djangoapps.onboarding.models import OrganizationMetricUpdatePrompt
from lms.djangoapps.onboarding.helpers import its_been_year, its_been_year_month, \
    its_been_year_three_month, its_been_year_six_month
from mailchimp_pipeline.signals.handlers import sync_metric_update_prompt_with_mail_chimp


from logging import getLogger
log = getLogger(__name__)


def is_prompt_values_are_same(prompt, year, year_month, year_three_month, year_six_month):
    """
    :param prompt: prompt object
    :param year: bool, updated year
    :param year_month: bool, updated year_month
    :param year_three_month: bool, updated_year_three_month
    :param year_six_month: bool, updated_year_six_month
    :return: True if any attribute of old and updated prompt and are not matching
    """
    return all((
        prompt.year == year,
        prompt.year_month == year_month,
        prompt.year_three_month == year_three_month,
        prompt.year_six_month == year_six_month
    ))


class Command(BaseCommand):
    help = """
    Update Organization Metric Prompts.
    And sync the updates with mailchimp
    """

    def handle(self, *args, **options):
        prompts = OrganizationMetricUpdatePrompt.objects.all()
        for prompt in prompts:
            submission_date = prompt.latest_metric_submission
            updated_year = its_been_year(submission_date)
            updated_year_month = its_been_year_month(submission_date)
            updated_year_three_month = its_been_year_three_month(submission_date)
            updated_year_six_month = its_been_year_six_month(submission_date)
            is_prompt_updated = is_prompt_values_are_same(prompt,
                                                          year=updated_year,
                                                          year_month=updated_year_month,
                                                          year_three_month=updated_year_three_month,
                                                          year_six_month=updated_year_six_month)

            if not is_prompt_updated:
                prompt.year = updated_year
                prompt.year_month = updated_year_month
                prompt.year_three_month = updated_year_three_month
                prompt.year_six_month = updated_year_six_month
                prompt.save()
                sync_metric_update_prompt_with_mail_chimp(prompt)
            else:
                log.info('No change detected')

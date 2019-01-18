"""
Handlers for onboarding app
"""
from django.db import connection

from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from mailchimp_pipeline.signals.handlers import sync_metric_update_prompt_with_mail_chimp
from lms.djangoapps.onboarding.models import Organization, OrganizationMetric,\
        OrganizationMetricUpdatePrompt
from lms.djangoapps.onboarding.helpers import its_been_year, its_been_year_month, \
    its_been_year_three_month, its_been_year_six_month


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, update_fields, **kwargs):
    user = instance
    user_profile = hasattr(user, 'profile') and user.profile

    # To avoid an extra sync at every login
    if (not update_fields or 'last_login' not in update_fields) and user_profile:
        user_profile.name = '{} {}'.format(user.first_name.encode('utf-8'), user.last_name.encode('utf-8'))
        user_profile.save()


@receiver(post_save, sender=OrganizationMetricUpdatePrompt)
def sync_metric_update_prompts_in_mailchimp(sender, instance, update_fields, **kwargs):
    # we can't put post_save on below method directly because it's being used
    # in a Data Migration, Management command too.
    sync_metric_update_prompt_with_mail_chimp(instance)


@receiver(post_save, sender=Organization)
def update_responsible_user_to_admin(instance, created, update_fields, **kwargs):
    if not created and 'admin_id' in update_fields:
        try:
            # TODO: clear the first responsible user in mailchimp after jassica's answer
            prompt = OrganizationMetricUpdatePrompt.objects.get(org_id=instance.org_id)
            prompt.admin_id = instance.admin_id
            prompt.save()
        except ObjectDoesNotExist:
            pass


@receiver(post_save, sender=OrganizationMetric)
def update_responsible_user_to_admin(instance, created, update_fields, **kwargs):
    this_metric_prompts = OrganizationMetricUpdatePrompt.objects.filter(org_id=instance.org_id)

    # Prepare date for prompt against this save in Organization Metric
    submission_date = instance.submission_date
    responsible_user = instance.org.admin or instance.user
    org = instance.org
    latest_metric_submission = instance.submission_date
    year = submission_date and its_been_year(submission_date)
    year_month = submission_date and its_been_year_month(submission_date)
    year_three_month = submission_date and its_been_year_three_month(submission_date)
    year_six_month = submission_date and its_been_year_six_month(submission_date)

    # If prompts against this Metric's already exists, update that prompt
    if len(this_metric_prompts):
        prompt = this_metric_prompts[0]
        prompt.responsible_user = responsible_user
        prompt.latest_metric_submission = latest_metric_submission
        prompt.year = year
        prompt.year_month = year_month
        prompt.year_three_month = year_three_month
        prompt.year_six_month = year_six_month
        prompt.save()
    else:
        # ceate a new prompt and save it
        prompt = OrganizationMetricUpdatePrompt(responsible_user=responsible_user,
                                                org=org,
                                                latest_metric_submission=latest_metric_submission,
                                                year=year,
                                                year_month=year_month,
                                                year_three_month=year_three_month,
                                                year_six_month=year_six_month
                                                )
        prompt.save()


@receiver(post_delete, sender=User)
def delete_all_user_data(sender, instance, **kwargs):

    cursor = connection.cursor()

    cursor.execute(
        'DELETE FROM auth_historicaluser WHERE id={};'.format(instance.id))
    cursor.execute(
        'DELETE FROM auth_historicaluserprofile WHERE user_id={};'.format(instance.id))
    cursor.execute(
        'DELETE FROM onboarding_historicaluserextendedprofile WHERE user_id={};'.format(instance.id))
    cursor.execute(
        'UPDATE onboarding_organization SET unclaimed_org_admin_email=NULL WHERE unclaimed_org_admin_email="{}"'.format(instance.email))
    cursor.execute(
        'UPDATE onboarding_organization SET alternate_admin_email=NULL WHERE alternate_admin_email="{}"'.format(instance.email))
    cursor.execute(
        'DELETE FROM onboarding_historicalorganization WHERE unclaimed_org_admin_email="{}" OR alternate_admin_email="{}"'.format(instance.email, instance.email))

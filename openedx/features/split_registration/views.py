"""
Views for on-boarding app.
"""
import base64
import json
import logging
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _, ugettext_noop
from django.views.decorators.csrf import csrf_exempt

from edxmako.shortcuts import render_to_response
from lms.djangoapps.onboarding.decorators import can_save_org_data, can_not_update_onboarding_steps, \
    can_save_org_details
from lms.djangoapps.onboarding.email_utils import send_admin_activation_email, send_admin_update_confirmation_email, \
    send_admin_update_email
from lms.djangoapps.onboarding.helpers import calculate_age_years, COUNTRIES, LANGUAGES, oef_eligible_first_learner, \
    get_close_matching_orgs_with_suggestions, get_alquity_community_url
from lms.djangoapps.onboarding.models import (
    Organization,
    Currency, OrganizationMetric, OrganizationAdminHashKeys, PartnerNetwork)
from lms.djangoapps.onboarding.models import UserExtendedProfile
from lms.djangoapps.onboarding.signals import save_interests
from lms.djangoapps.student_dashboard.views import get_recommended_xmodule_courses, get_joined_communities
from nodebb.helpers import update_nodebb_for_user_status
from openedx.features.split_registration import forms

log = logging.getLogger("edx.onboarding")


@login_required
@can_not_update_onboarding_steps
@transaction.atomic
def user_info(request):
    """
    The view to handle user info survey from the user.

    If its a GET request then an empty form for survey is returned
    otherwise, a form is populated form the POST request data and
    is then saved. After saving the form, user is redirected to the
    next survey namely, interests survey.
    """

    user_extended_profile = request.user.extended_profile
    are_forms_complete = not (bool(user_extended_profile.unattended_surveys_v2(_type='list')))
    userprofile = request.user.profile
    is_under_age = False

    template = 'features/onboarding/tell_us_more_survey.html'
    redirect_to_next = True

    if request.path == reverse('additional_information'):
        redirect_to_next = False
        template = 'features/account/additional_information.html'

    initial = {
        'year_of_birth': userprofile.year_of_birth,
        'gender': userprofile.gender,
        'language': userprofile.language,
        'country': COUNTRIES.get(userprofile.country) if not request.POST.get('country') else request.POST.get('country'),
        'city': userprofile.city,
        'level_of_education': userprofile.level_of_education,
        'organization_name': user_extended_profile.organization.label if user_extended_profile.organization else "",
        'is_poc': "1" if user_extended_profile.is_organization_admin else "0",
    }

    context = {
        'are_forms_complete': are_forms_complete, 'first_name': request.user.first_name,
        'fields_to_disable': []
    }

    year_of_birth = userprofile.year_of_birth

    if request.method == 'POST':
        year_of_birth = request.POST.get('year_of_birth')

    if year_of_birth:
        years = calculate_age_years(int(year_of_birth))
        if years < 16:
            is_under_age = True

    if request.method == 'POST':
        form = forms.UserInfoModelForm(request.POST, instance=user_extended_profile, initial=initial)

        if form.is_valid() and not is_under_age:
            custom_model = form.save(request)

            if custom_model.organization:
                custom_model.organization.save()

            unattended_surveys = user_extended_profile.unattended_surveys_v2(_type='list')
            are_forms_complete = not (bool(unattended_surveys))

            if not are_forms_complete and redirect_to_next:
                return redirect(unattended_surveys[0])

            # this will only executed if user updated his/her employed status from account settings page
            # redirect user to account settings page where he come from
            if not request.path == "/user-account/additional_information/":
                return redirect(reverse("update_account"))

    else:
        form = forms.UserInfoModelForm(instance=user_extended_profile, initial=initial)

    # if org_name and admin_email:
    #     org_name = base64.b64decode(org_name)
    #     admin_email = base64.b64decode(admin_email)
    #
    #     email_field = get_form_field_by_name(registration_fields, 'email')
    #     org_field = get_form_field_by_name(registration_fields, 'organization_name')
    #     is_poc_field = get_form_field_by_name(registration_fields, 'is_poc')
    #     email_field['defaultValue'] = admin_email
    #     org_field['defaultValue'] = org_name
    #     is_poc_field['defaultValue'] = "1"
    #
    #     context['fields_to_disable'] = json.dumps([email_field['name'], org_field['name'], is_poc_field['name']])

    context.update({
        'form': form,
        'is_under_age': is_under_age,
        'non_profile_organization': Organization.is_non_profit(user_extended_profile),
        'is_poc': user_extended_profile.is_organization_admin,
        'is_first_user': user_extended_profile.is_first_signup_in_org if user_extended_profile.organization else False,
        'google_place_api_key': settings.GOOGLE_PLACE_API_KEY,
        'org_url': reverse('get_organizations')

    })

    context.update(user_extended_profile.unattended_surveys())
    return render(request, template, context)


@login_required
@can_not_update_onboarding_steps
@transaction.atomic
def interests(request):
    """
    The view to handle interests survey from the user.

    If its a GET request then an empty form for survey is returned
    otherwise, a form is populated form the POST request and then is
    saved. After saving the form, user is redirected to the next survey
    namely, organization survey.
    """
    user_extended_profile = request.user.extended_profile
    are_forms_complete = not(bool(user_extended_profile.unattended_surveys_v2(_type='list')))

    template = 'features/onboarding/interests_survey.html'
    redirect_to_next = True

    if request.path == reverse('update_interests'):
        redirect_to_next = False
        template = 'features/account/interests.html'

    initial = {
        "interests": user_extended_profile.get_user_selected_interests(_type="fields"),
        "interested_learners": user_extended_profile.get_user_selected_interested_learners(_type="fields"),
        "personal_goals": user_extended_profile.get_user_selected_personal_goal(_type="fields"),
        "hear_about_philanthropy":  user_extended_profile.get_user_hear_about_philanthropy(_type="fields"),
        "hear_about_philanthropy_other":  user_extended_profile.hear_about_philanthropy_other if user_extended_profile
                                          .hear_about_philanthropy_other else ''
    }

    if request.method == 'POST':
        form = forms.InterestsForm(request.POST, initial=initial)

        is_action_update = user_extended_profile.is_interests_data_submitted

        form.save(request, user_extended_profile)

        save_interests.send(sender=UserExtendedProfile, instance=user_extended_profile)

        are_forms_complete = not (bool(user_extended_profile.unattended_surveys_v2(_type='list')))

        are_org_forms_complete = not (bool(user_extended_profile.org_unattended_surveys_v2(_type='list')))
        org_unattended_surveys = user_extended_profile.org_unattended_surveys_v2(_type='list')

        if request.POST.get('next') == 'organization' and redirect_to_next and not are_org_forms_complete:
            return redirect(reverse(org_unattended_surveys[0]))

        if are_forms_complete and not is_action_update:
            update_nodebb_for_user_status(request.user.username)
            if user_extended_profile.is_alquity_user:
                return redirect(get_alquity_community_url())
            return redirect(reverse('recommendations'))

    else:
        form = forms.InterestsForm(initial=initial)
    context = {'form': form, 'are_forms_complete': are_forms_complete}

    user = request.user
    extended_profile = user.extended_profile
    context.update(extended_profile.unattended_surveys())
    is_employed = bool(user.extended_profile.organization)
    is_first_signup_in_org = user_extended_profile.is_first_signup_in_org \
        if user_extended_profile.organization else False

    context.update({
        'non_profile_organization': Organization.is_non_profit(user_extended_profile),
        'is_employed': is_employed,
        'organization_name': user.extended_profile.organization.label if is_employed else '',
        'user_fullname': user.profile.name,
        'is_poc': extended_profile.is_organization_admin,
        'is_first_user': is_first_signup_in_org
    })

    return render(request, template, context)


@login_required
@can_not_update_onboarding_steps
@transaction.atomic
def user_organization_role(request):
    """
    The view to handle user info survey from the user.

    If its a GET request then an empty form for survey is returned
    otherwise, a form is populated form the POST request data and
    is then saved. After saving the form, user is redirected to the
    next survey namely, interests survey.
    """

    user_extended_profile = request.user.extended_profile
    are_forms_complete = not (bool(user_extended_profile.org_unattended_surveys_v2(_type='list')))

    template = 'features/onboarding/organization_role.html'
    redirect_to_next = True

    if request.path == reverse('additional_information'):
        redirect_to_next = False
        template = 'features/account/additional_information.html'

    initial = {
        'country_of_employment': COUNTRIES.get(user_extended_profile.country_of_employment, '') if not request.POST.get('country_of_employment') else request.POST.get('country_of_employment') ,
        'hours_per_week': user_extended_profile.hours_per_week if user_extended_profile.hours_per_week else '',
        'is_emp_location_different': True if user_extended_profile.country_of_employment else False,
        "function_areas": user_extended_profile.get_user_selected_functions(_type="fields")
    }

    context = {
        'are_forms_complete': are_forms_complete, 'first_name': request.user.first_name
    }

    if request.method == 'POST':
        form = forms.OrganizationRoleForm(request.POST, instance=user_extended_profile, initial=initial)

        if form.is_valid():
            form.save(request, user_extended_profile)
            unattended_surveys = user_extended_profile.org_unattended_surveys_v2(_type='list')
            are_forms_complete = not (bool(unattended_surveys))

            if not are_forms_complete and redirect_to_next:
                return redirect(unattended_surveys[0])

            if are_forms_complete:
                update_nodebb_for_user_status(request.user.username)
                return redirect(reverse('recommendations'))

            # this will only executed if user updated his/her employed status from account settings page
            # redirect user to account settings page where he come from
            # if not request.path == "features/account/additional_information/":
            #     return redirect(reverse("update_account_settings"))

    else:
        form = forms.OrganizationRoleForm(instance=user_extended_profile, initial=initial)

    context.update({
        'form': form,
        'non_profile_organization': Organization.is_non_profit(user_extended_profile),
        'is_poc': user_extended_profile.is_organization_admin,
        'is_employed': bool(user_extended_profile.organization),
        'is_first_user': user_extended_profile.is_first_signup_in_org if user_extended_profile.organization else False,
        'google_place_api_key': settings.GOOGLE_PLACE_API_KEY,
    })

    context.update(user_extended_profile.unattended_surveys())
    return render(request, template, context)


@login_required
@can_save_org_data
@can_not_update_onboarding_steps
@transaction.atomic
def organization(request):
    """
    The view to handle organization survey from the user.

    If its a GET request then an empty form for survey is returned
    otherwise, a form is populated form the POST request and then is
    saved. After saving the form, user is redirected to recommendations page.
    """
    user_extended_profile = request.user.extended_profile
    _organization = user_extended_profile.organization
    are_forms_complete = not(bool(user_extended_profile.org_unattended_surveys_v2(_type='list')))

    template = 'features/onboarding/organization_survey.html'
    next_page_url = reverse('recommendations')
    redirect_to_next = True

    if request.path == reverse('update_organization'):
        redirect_to_next = False
        template = 'features/organization/update_organization.html'

    initial = {
        'country': COUNTRIES.get(_organization.country),
        'is_org_url_exist': '1' if _organization.url else '0',
        'partner_networks': _organization.get_active_partners(),
    }

    if request.method == 'POST':
        old_url = request.POST.get('url', '').replace('http://', 'https://', 1)
        form = forms.OrganizationInfoForm(request.POST, instance=_organization, initial=initial)

        if form.is_valid():
            form.save(request)
            old_url = _organization.url.replace('https://', '', 1) if _organization.url else _organization.url
            org_unattended_user_surveys = user_extended_profile.org_unattended_surveys_v2(_type='list')
            are_forms_complete = not (bool(org_unattended_user_surveys))

            if not are_forms_complete:
                # redirect to organization detail page
                next_page_url = reverse(org_unattended_user_surveys[0])
            else:
                # update nodebb for user profile completion
                update_nodebb_for_user_status(request.user.username)

            if redirect_to_next:
                return redirect(next_page_url)

    else:
        old_url = _organization.url.replace('https://', '', 1) if _organization.url else _organization.url
        form = forms.OrganizationInfoForm(instance=_organization, initial=initial)

    context = {'form': form, 'are_forms_complete': are_forms_complete, 'old_url': old_url}

    organization = user_extended_profile.organization
    context.update(user_extended_profile.unattended_surveys())

    context.update({
        'non_profile_organization': Organization.is_non_profit(user_extended_profile),
        'is_employed': bool(user_extended_profile.organization),
        'is_poc': user_extended_profile.is_organization_admin,
        'is_first_user': user_extended_profile.is_first_signup_in_org if user_extended_profile.organization else False,
        'org_admin_id': organization.admin_id if user_extended_profile.organization else None,
        'organization_name': _organization.label,
        'google_place_api_key': settings.GOOGLE_PLACE_API_KEY
    })

    return render(request, template, context)


@login_required
@can_save_org_details
@can_not_update_onboarding_steps
@transaction.atomic
def org_detail_survey(request):
    user_extended_profile = request.user.extended_profile
    are_forms_complete = not(bool(user_extended_profile.unattended_surveys(_type='list')))
    latest_survey = OrganizationMetric.objects.filter(org=user_extended_profile.organization).last()

    initial = {
        'actual_data': '1' if latest_survey and latest_survey.actual_data else '0',
        'registration_number': user_extended_profile.organization.registration_number if user_extended_profile.organization else '',
        "effective_date": datetime.strftime(latest_survey.effective_date, '%m/%d/%Y') if latest_survey else ""
    }

    template = 'features/onboarding/organization_detail_survey.html'
    next_page_url = reverse('recommendations')
    org_metric_form = forms.OrganizationMetricModelForm
    redirect_to_next = True

    if request.path == reverse('update_organization_details'):
        redirect_to_next = False
        template = 'features/organization/update_organization_details.html'
        org_metric_form = forms.OrganizationMetricModelUpdateForm

    if request.method == 'POST':
        available_next = request.POST.get('next', None)
        is_user_coming_from_overlay = available_next and available_next == 'oef'

        if is_user_coming_from_overlay:
            redirect_to_next = True

        if latest_survey:
            form = org_metric_form(request.POST, instance=latest_survey, initial=initial)
        else:
            form = org_metric_form(request.POST, initial=initial)

        if form.is_valid():
            form.save(request)

            are_forms_complete = not (bool(user_extended_profile.org_unattended_surveys_v2(_type='list')))

            if are_forms_complete and redirect_to_next:
                update_nodebb_for_user_status(request.user.username)

                if is_user_coming_from_overlay:
                    next_page_url = reverse('oef_dashboard')

                return redirect(next_page_url)

    else:
        if latest_survey:
            form = org_metric_form(instance=latest_survey, initial=initial)
        else:
            form = org_metric_form()

    next_url = request.GET.get('next', None)
    context = {'form': form, 'are_forms_complete': are_forms_complete, 'next': next_url}
    context.update(user_extended_profile.org_unattended_surveys_v2())

    context.update({
        'non_profile_organization': Organization.is_non_profit(user_extended_profile),
        'is_poc': user_extended_profile.is_organization_admin,
        'is_first_user': user_extended_profile.is_first_signup_in_org if user_extended_profile.organization else False,
        'organization_name': user_extended_profile.organization.label,
        'is_employed': bool(user_extended_profile.organization)
    })

    return render(request, template, context)


@login_required
def update_account_settings(request):
    """
    View to handle update of registration extra fields
    """

    user_extended_profile = UserExtendedProfile.objects.get(user_id=request.user.id)
    if request.method == 'POST':

        form = forms.UpdateRegModelForm(request.POST, instance=user_extended_profile)
        if form.is_valid():
            user_extended_profile = form.save(user=user_extended_profile.user, commit=True)
            unattended_surveys = user_extended_profile.unattended_surveys_v2(_type='list')
            are_forms_complete = not (bool(unattended_surveys))

            if not are_forms_complete:
                return redirect(reverse(unattended_surveys[0]))

            return redirect(reverse('update_account'))

    else:
        email_preferences = getattr(request.user, 'email_preferences', None)
        form = forms.UpdateRegModelForm(
            instance=user_extended_profile,
            initial={
                'first_name': user_extended_profile.user.first_name,
                'last_name': user_extended_profile.user.last_name,
                'opt_in': email_preferences.opt_in if email_preferences else ''
            }
        )

    ctx = {
        'form': form,
    }

    return render(request, 'features/account/registration_update.html', ctx)

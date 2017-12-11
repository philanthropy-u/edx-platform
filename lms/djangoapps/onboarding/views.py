"""
Views for on-boarding app.
"""
import json
import logging
import base64

import os
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from path import Path as path

from edxmako.shortcuts import render_to_response
from lms.djangoapps.onboarding.helpers import calculate_age_years, COUNTRIES
from lms.djangoapps.onboarding.models import (
    Organization,
    Currency, OrganizationMetric)
from lms.djangoapps.student_dashboard.views import get_recommended_xmodule_courses, get_recommended_communities
from onboarding import forms
from lms.djangoapps.onboarding.models import UserExtendedProfile

log = logging.getLogger("edx.onboarding")


@login_required
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
    are_forms_complete = not (bool(user_extended_profile.unattended_surveys(_type='list')))
    userprofile = request.user.profile
    is_under_age = False

    initial = {
        'year_of_birth': userprofile.year_of_birth,
        'gender': userprofile.gender,
        'language': userprofile.language,
        'country': COUNTRIES.get(userprofile.country),
        'city': userprofile.city,
        "function_areas": user_extended_profile.get_user_selected_functions(_type="fields")
    }

    context = {
        'are_forms_complete': are_forms_complete, 'first_name': request.user.first_name
    }

    year_of_birth = userprofile.year_of_birth

    if request.method == 'POST':
        year_of_birth = request.POST.get('year_of_birth')

    if year_of_birth:
        years = calculate_age_years(int(year_of_birth))
        if years < 18:
            is_under_age = True

    if request.method == 'POST':
        form = forms.UserInfoModelForm(request.POST, instance=user_extended_profile, initial=initial)

        if form.is_valid() and not is_under_age:
            form.save(request)

            are_forms_complete = not (bool(user_extended_profile.unattended_surveys(_type='list')))

            if not are_forms_complete:
                return redirect(reverse('interests'))
            return redirect(reverse('user_info'))

    else:
        form = forms.UserInfoModelForm(instance=user_extended_profile, initial=initial)

    context.update({
        'form': form,
        'is_under_age': is_under_age,
        'is_poc': user_extended_profile.is_organization_admin,
        'is_first_user': user_extended_profile.organization.is_first_signup_in_org(),
        'google_place_api_key': settings.GOOGLE_PLACE_API_KEY
    })

    context.update(user_extended_profile.unattended_surveys())
    return render(request, 'onboarding/tell_us_more_survey.html', context)


@login_required
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
    are_forms_complete = not(bool(user_extended_profile.unattended_surveys()))
    is_first_signup_in_org = user_extended_profile.organization.is_first_signup_in_org()

    initial = {
        "interests": user_extended_profile.get_user_selected_interests(_type="fields"),
        "interested_learners": user_extended_profile.get_user_selected_interested_learners(_type="fields"),
        "personal_goals": user_extended_profile.get_user_selected_personal_goal(_type="fields")
    }

    if request.method == 'POST':
        form = forms.InterestsForm(request.POST, initial=initial)

        interest_survey = form.save(request, user_extended_profile)

        # save_interests.send(sender=InterestsSurvey, instance=interest_survey)

        if user_extended_profile.is_organization_admin or is_first_signup_in_org:
            return redirect(reverse('organization'))

        if are_forms_complete:
            return redirect(reverse('recommendations'))

        return redirect(reverse('interests'))

    else:
        form = forms.InterestsForm(initial=initial)

    context = {'form': form, 'are_forms_complete': are_forms_complete}

    user = request.user
    extended_profile = user.extended_profile
    context.update(extended_profile.unattended_surveys())
    context['is_poc'] = extended_profile.is_organization_admin
    context['is_first_user'] = is_first_signup_in_org
    return render(request, 'onboarding/interests_survey.html', context)


@login_required
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
    are_forms_complete = not(bool(user_extended_profile.unattended_surveys(_type='list')))

    initial = {
        'country': COUNTRIES.get(_organization.country),
    }

    if request.method == 'POST':
        form = forms.OrganizationInfoForm(request.POST, instance=_organization, initial=initial)

        if form.is_valid():
            form.save(request)

            are_forms_complete = not (bool(user_extended_profile.unattended_surveys(_type='list')))

            if not are_forms_complete:
                return redirect(reverse('org_detail_survey'))

            return redirect(reverse('organization'))

    else:
        form = forms.OrganizationInfoForm(instance=_organization, initial=initial)

    context = {'form': form, 'are_forms_complete': are_forms_complete}

    context.update(user_extended_profile.unattended_surveys())
    context['is_poc'] = user_extended_profile.is_organization_admin
    context['is_first_user'] = user_extended_profile.organization.is_first_signup_in_org()
    context['organization_name'] = _organization.label
    context['google_place_api_key'] = settings.GOOGLE_PLACE_API_KEY

    return render(request, 'onboarding/organization_survey.html', context)

@login_required
def delete_my_account(request):
    user = request.user
    user_extended_profile = user.extended_profile

    surveys_to_attend = user_extended_profile.surveys_to_attend()

    if user.is_active and len(user_extended_profile.unattended_surveys(_type='list')) == len(surveys_to_attend):
        logout(request)

        User.objects.filter(id=user.id).delete()

        data = json.dumps({"status": 200})
    else:
        data = json.dumps({"status": 400})

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)



@csrf_exempt
def get_country_names(request):
    """
    Returns country names.
    """
    if request.is_ajax():
        q = request.GET.get('term', '')
        all_countries = COUNTRIES.values()

        filtered_countries = [country for country in all_countries if country.lower().startswith(q.lower())]

        data = json.dumps(filtered_countries)

    else:
        data = 'fail'

    mime_type = 'application/json'

    return HttpResponse(data, mime_type)


@login_required
@transaction.atomic
def org_detail_survey(request):
    user_extended_profile = request.user.extended_profile
    are_forms_complete = not(bool(user_extended_profile.unattended_surveys(_type='list')))

    latest_survey = OrganizationMetric.objects.filter(org=user_extended_profile.organization,
                                                      user=request.user).last()

    if request.method == 'POST':

        if latest_survey:
            form = forms.OrganizationMetricModelForm(request.POST, instance=latest_survey)
        else:
            form = forms.OrganizationMetricModelForm(request.POST)

        if form.is_valid():
            form.save(request)

            are_forms_complete = not (bool(user_extended_profile.unattended_surveys(_type='list')))

            if are_forms_complete:
                return redirect(reverse('oef_instructions'))

            return redirect(reverse('org_detail_survey'))

    else:
        if latest_survey:
            form = forms.OrganizationMetricModelForm(instance=latest_survey, initial={
                'can_provide_info': '1' if latest_survey else '0',
                'actual_data': '1' if latest_survey.actual_data else '0',
            })
        else:
            form = forms.OrganizationMetricModelForm()

    context = {'form': form, 'are_forms_complete': are_forms_complete}
    context.update(user_extended_profile.unattended_surveys())
    context['is_poc'] = user_extended_profile.is_organization_admin
    context['is_first_user'] = user_extended_profile.organization.is_first_signup_in_org()
    context['organization_name'] = user_extended_profile.organization.label
    return render(request, 'onboarding/organization_detail_survey.html', context)


@csrf_exempt
def get_languages(request):
    """
    Returns languages
    """
    if request.is_ajax():
        file_path = path(os.path.join(
            'lms', 'djangoapps', 'onboarding', 'data', 'world_languages.json'
        )).abspath()
        with open(file_path) as json_data:
            q = request.GET.get('term', '')
            all_languages = json.load(json_data)
            filtered_languages = [language for language in all_languages if language.lower().startswith(q.lower())]

        data = json.dumps(filtered_languages)

    else:
        data = 'fail'

    mime_type = 'application/json'

    return HttpResponse(data, mime_type)


@login_required
def update_account_settings(request):
    """
    View to handle update of registration extra fields
    """
    user_extended_profile = request.user.extended_profile
    if request.method == 'POST':

        form = forms.UpdateRegModelForm(request.POST, instance=user_extended_profile)
        if form.is_valid():
            form_instance = form.save(commit=False)
            if form_instance.is_poc:
                form_instance.org_admin_email = ""
            form_instance.save()

    else:
        form = forms.UpdateRegModelForm(
            instance=user_extended_profile,
            initial={
                'organization_name': user_extended_profile.organization.label,
                'is_poc': 1 if user_extended_profile.is_organization_admin else 0
            }
        )

    return render(
        request, 'onboarding/registration_update.html',
        {'form': form, 'org_url': reverse('get_user_organizations')}
    )


@csrf_exempt
def get_user_organizations(request):
    """
    Get organizations
    """
    final_result = {}
    if request.is_ajax():
        query = request.GET.get('term', '')
        all_organizations = Organization.objects.filter(label__istartswith=query)
        for organization in all_organizations:
            final_result[organization.label] = True if organization.admin else False

        if request.user.is_authenticated():
            user_extended_profile = request.user.extended_profile
            final_result['user_org_info'] = {
                'org': user_extended_profile.organization.label,
                'admin_email': user_extended_profile.org_admin_email
            }

    return JsonResponse(final_result)


@csrf_exempt
def get_currencies(request):
    currencies = []

    if request.is_ajax():
        term = request.GET.get('term', '')
        currencies = Currency.objects.filter(alphabetic_code__istartswith=term).values_list('alphabetic_code',
                                                                                            flat=True).distinct()
    data = json.dumps(list(currencies))
    return HttpResponse(data, 'application/json')


@login_required
def recommendations(request):
    """
    Display recommended courses and communities based on the survey

    """
    recommended_courses = get_recommended_xmodule_courses(request.user)
    recommended_communities = get_recommended_communities(request.user)
    context = {
        'recommended_courses': recommended_courses,
        'recommended_communities': recommended_communities,
    }

    return render_to_response('onboarding/recommendations.html', context)

@csrf_exempt
def admin_activation(request, org_id, activation_key):
    """
    When clicked on link sent in email to make user admin.

    """
    extended_profile = None
    try:
        extended_profile = UserExtendedProfile.objects.get(admin_activation_key=activation_key)
    except UserExtendedProfile.DoesNotExist:
        pass
    # activation_status can have values 1,2,3,4.
    # 1 means 'activated',
    # 2 means 'already active',
    # 3 means 'Invalid key',
    # 4 means 'to be activated'
    context = {}
    activation_status = 3
    if extended_profile:
        if extended_profile.is_admin_activated:
            activation_status = 2
        elif request.method == 'GET':
            context['key'] = extended_profile.admin_activation_key
            activation_status = 4
        elif request.method == 'POST':
            try:
                decoded_org_id = base64.b64decode(org_id)
                organization = Organization.objects.get(pk=decoded_org_id)
                extended_profile.is_admin_activated = True
                extended_profile.is_poc = True
                extended_profile.organization = organization
                organization.admin = extended_profile.user
                extended_profile.save()
                activation_status = 1
                organization.save()
            except Organization.DoesNotExist:
                activation_status = 3
            except Exception:
                activation_status = 3

    context['activation_status'] = activation_status
    return render_to_response('onboarding/admin_activation.html', context)

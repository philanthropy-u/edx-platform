from lms.djangoapps.onboarding.models import UserExtendedProfile


def get_un_submitted_surveys(user_extended_profile):
    """
    Get the info about the un-submitted forms
    """
    un_submitted_surveys = {}
    if not user_extended_profile.is_first_survey_attended:
        un_submitted_surveys['user_info'] = True

    try:
        user.interest_survey
    except Exception:
        un_submitted_surveys['interests'] = True

    try:
        user.organization_survey
    except Exception:
        un_submitted_surveys['organization'] = True

    try:
        user.org_detail_survey
    except Exception:
        un_submitted_surveys['org_detail_survey'] = True

    if un_submitted_surveys.get('user_info') and un_submitted_surveys.get('interests') and\
            un_submitted_surveys.get('organization') and un_submitted_surveys.get('org_detail_survey'):
        un_submitted_surveys['user_info'] = False

    elif un_submitted_surveys.get('interests') and un_submitted_surveys.get('organization')\
            and un_submitted_surveys.get('org_detail_survey'):
        un_submitted_surveys['user_info'] = False
        un_submitted_surveys['interests'] = False

    elif un_submitted_surveys.get('organization') and un_submitted_surveys.get('org_detail_survey'):
        un_submitted_surveys['user_info'] = False
        un_submitted_surveys['interests'] = False
        un_submitted_surveys['organization'] = False
    else:
        un_submitted_surveys['user_info'] = False
        un_submitted_surveys['interests'] = False
        un_submitted_surveys['organization'] = False
        un_submitted_surveys['org_detail_survey'] = False

    return un_submitted_surveys

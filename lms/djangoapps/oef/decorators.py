from django.core.exceptions import PermissionDenied

from lms.djangoapps.onboarding.models import PartnerNetwork


def can_take_oef(function):
    def wrap(request, *args, **kwargs):
        user_extended_profile = request.user.extended_profile

        if user_extended_profile.organization and user_extended_profile.organization.is_non_profit and  \
                (user_extended_profile.is_organization_admin or
                     (user_extended_profile.is_first_signup_in_org and not user_extended_profile.has_submitted_oef())):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


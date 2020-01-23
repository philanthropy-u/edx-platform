"""
Utility functions for validating forms
"""
import re
from importlib import import_module

from django import forms
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.validators import RegexValidator, slug_re
from django.forms import widgets
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from edx_ace import ace
from edx_ace.recipient import Recipient
from lms.djangoapps.onboarding.models import Organization, OrgSector, TotalEmployee
from openedx.core.djangoapps.ace_common.template_context import get_base_template_context
from openedx.core.djangoapps.lang_pref import LANGUAGE_KEY
from openedx.core.djangolib.markup import HTML, Text
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.theming.helpers import get_current_site
from openedx.core.djangoapps.user_api import accounts as accounts_settings
from openedx.core.djangoapps.user_api.preferences.api import get_user_preference
from student.message_types import AccountRecovery as AccountRecoveryMessage, PasswordReset
from student.models import AccountRecovery, CourseEnrollmentAllowed, email_exists_or_retired
from util.password_policy_validators import validate_password
from common.lib.mandrill_client.client import MandrillClient


def send_password_reset_email_for_user(user, request, preferred_email=None):
    """
    Send out a password reset email for the given user.

    Arguments:
        user (User): Django User object
        request (HttpRequest): Django request object
        preferred_email (str): Send email to this address if present, otherwise fallback to user's email address.
    """
    site_name = configuration_helpers.get_value(
        'SITE_NAME',
        settings.SITE_NAME
    )

    password_reset_link = '{protocol}://{site_name}{reset_link}'.format(
        protocol='https' if request.is_secure() else 'http',
        site_name=site_name,
        reset_link=reverse('password_reset_confirm', kwargs={
            'uidb36': int_to_base36(user.id),
            'token': default_token_generator.make_token(user),
        })
    )

    MandrillClient().send_mail(MandrillClient.PASSWORD_RESET_TEMPLATE, user.email, {
        'first_name': user.first_name,
        'reset_link': password_reset_link,
    })


def send_account_recovery_email_for_user(user, request, email=None):
    """
    Send out a account recovery email for the given user.

    Arguments:
        user (User): Django User object
        request (HttpRequest): Django request object
        email (str): Send email to this address.
    """
    site = get_current_site()
    message_context = get_base_template_context(site)
    message_context.update({
        'request': request,  # Used by google_analytics_tracking_pixel
        'platform_name': configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME),
        'reset_link': '{protocol}://{site}{link}'.format(
            protocol='https' if request.is_secure() else 'http',
            site=configuration_helpers.get_value('SITE_NAME', settings.SITE_NAME),
            link=reverse('account_recovery_confirm', kwargs={
                'uidb36': int_to_base36(user.id),
                'token': default_token_generator.make_token(user),
            }),
        )
    })

    msg = AccountRecoveryMessage().personalize(
        recipient=Recipient(user.username, email),
        language=get_user_preference(user, LANGUAGE_KEY),
        user_context=message_context,
    )
    ace.send(msg)


class PasswordResetFormNoActive(PasswordResetForm):
    error_messages = {
        'unknown': _("That e-mail address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': _("The user account associated with this e-mail "
                      "address cannot reset the password."),
    }

    def clean_email(self):
        """
        This is a literal copy from Django 1.4.5's django.contrib.auth.forms.PasswordResetForm
        Except removing the requirement of active users
        Validates that a user exists with the given email address.
        """
        email = self.cleaned_data["email"]
        #The line below contains the only change, removing is_active=True
        self.users_cache = User.objects.filter(email__iexact=email)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password.startswith(UNUSABLE_PASSWORD_PREFIX))
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self,  # pylint: disable=arguments-differ
             use_https=False,
             token_generator=default_token_generator,
             request=None,
             **_kwargs):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            send_password_reset_email_for_user(user, request)


class AccountRecoveryForm(PasswordResetFormNoActive):
    error_messages = {
        'unknown': _(
            HTML(
                'That secondary e-mail address doesn\'t have an associated user account. Are you sure you had added '
                'a verified secondary email address for account recovery in your account settings? Please '
                '<a href={support_url}">contact support</a> for further assistance.'
            )
        ).format(
            support_url=configuration_helpers.get_value('SUPPORT_SITE_LINK', settings.SUPPORT_SITE_LINK),
        ),
        'unusable': _(
            Text(
                'The user account associated with this secondary e-mail address cannot reset the password.'
            )
        ),
    }

    def clean_email(self):
        """
        This is a literal copy from Django's django.contrib.auth.forms.PasswordResetForm
        Except removing the requirement of active users
        Validates that a user exists with the given secondary email.
        """
        email = self.cleaned_data["email"]
        # The line below contains the only change, getting users via AccountRecovery
        self.users_cache = User.objects.filter(
            id__in=AccountRecovery.objects.filter(secondary_email__iexact=email, is_active=True).values_list('user')
        )

        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password.startswith(UNUSABLE_PASSWORD_PREFIX))
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self,  # pylint: disable=arguments-differ
             use_https=False,
             token_generator=default_token_generator,
             request=None,
             **_kwargs):
        """
        Generates a one-use only link for setting the password and sends to the
        user.
        """
        for user in self.users_cache:
            send_account_recovery_email_for_user(user, request, user.account_recovery.secondary_email)


class TrueCheckbox(widgets.CheckboxInput):
    """
    A checkbox widget that only accepts "true" (case-insensitive) as true.
    """
    def value_from_datadict(self, data, files, name):
        value = data.get(name, '')
        return value.lower() == 'true'


class TrueField(forms.BooleanField):
    """
    A boolean field that only accepts "true" (case-insensitive) as true
    """
    widget = TrueCheckbox


def validate_username(username):
    """
    Verifies a username is valid, raises a ValidationError otherwise.
    Args:
        username (unicode): The username to validate.

    This function is configurable with `ENABLE_UNICODE_USERNAME` feature.
    """

    username_re = slug_re
    flags = None
    message = accounts_settings.USERNAME_INVALID_CHARS_ASCII

    if settings.FEATURES.get("ENABLE_UNICODE_USERNAME"):
        username_re = r"^{regex}$".format(regex=settings.USERNAME_REGEX_PARTIAL)
        flags = re.UNICODE
        message = accounts_settings.USERNAME_INVALID_CHARS_UNICODE

    validator = RegexValidator(
        regex=username_re,
        flags=flags,
        message=message,
        code='invalid',
    )

    validator(username)


def contains_html(value):
    """
    Validator method to check whether name contains html tags
    """
    regex = re.compile('(<|>)', re.UNICODE)
    return bool(regex.search(value))


def validate_name(name):
    """
    Verifies a Full_Name is valid, raises a ValidationError otherwise.
    Args:
        name (unicode): The name to validate.
    """
    if contains_html(name):
        raise forms.ValidationError(_('Full Name cannot contain the following characters: < >'))


def validate_org_size(org_size):
    possible_org_sizes = [total_employee.code for total_employee in TotalEmployee.objects.all()]
    if org_size not in possible_org_sizes:
        raise forms.ValidationError(_('Invalid org size option provided'))


def validate_org_type(org_type):
    possible_org_types = [org_sector.code for org_sector in OrgSector.objects.all()]
    if org_type not in possible_org_types:
        raise forms.ValidationError(_('Invalid org type option provided'))


def validate_opt_in_choice(opt_in):
    possible_opt_in_options = ["yes", "no"]
    if opt_in not in possible_opt_in_options:
        raise forms.ValidationError(_('Invalid email opt in option provided'))


class UsernameField(forms.CharField):
    """
    A CharField that validates usernames based on the `ENABLE_UNICODE_USERNAME` feature.
    """

    default_validators = [validate_username]

    def __init__(self, *args, **kwargs):
        super(UsernameField, self).__init__(
            min_length=accounts_settings.USERNAME_MIN_LENGTH,
            max_length=accounts_settings.USERNAME_MAX_LENGTH,
            error_messages={
                "required": accounts_settings.USERNAME_BAD_LENGTH_MSG,
                "min_length": accounts_settings.USERNAME_BAD_LENGTH_MSG,
                "max_length": accounts_settings.USERNAME_BAD_LENGTH_MSG,
            }
        )

    def clean(self, value):
        """
        Strips the spaces from the username.

        Similar to what `django.forms.SlugField` does.
        """

        value = self.to_python(value).strip()
        return super(UsernameField, self).clean(value)


class AccountCreationForm(forms.Form):
    """
    A form for account creation data. It is currently only used for
    validation, not rendering.
    """

    _EMAIL_INVALID_MSG = _("A properly formatted e-mail is required")
    _NAME_TOO_SHORT_MSG = _("Your legal name must be a minimum of two characters long")
    _OPT_IN_REQUIRED_MSG = _("Email opt in is a required field, and can only be set to true or false")

    # TODO: Resolve repetition

    username = UsernameField()

    email = forms.EmailField(
        max_length=accounts_settings.EMAIL_MAX_LENGTH,
        min_length=accounts_settings.EMAIL_MIN_LENGTH,
        error_messages={
            "required": _EMAIL_INVALID_MSG,
            "invalid": _EMAIL_INVALID_MSG,
            "max_length": _("Email cannot be more than %(limit_value)s characters long"),
        }
    )

    password = forms.CharField()

    first_name = forms.CharField(
        min_length=accounts_settings.NAME_MIN_LENGTH,
        error_messages={
            "required": _NAME_TOO_SHORT_MSG,
            "min_length": _NAME_TOO_SHORT_MSG,
        },
        validators=[validate_name]
    )

    last_name = forms.CharField(
        min_length=accounts_settings.NAME_MIN_LENGTH,
        error_messages={
            "required": _NAME_TOO_SHORT_MSG,
            "min_length": _NAME_TOO_SHORT_MSG,
        },
        validators=[validate_name]
    )

    org_size = forms.CharField(
        required=False,
        validators=[validate_org_size]
    )

    org_type = forms.CharField(
        required=False,
        validators=[validate_org_type]
    )

    org_name = forms.CharField(
        required=False
    )

    opt_in = forms.CharField(
        error_messages={
            "required": _OPT_IN_REQUIRED_MSG,
        },
        validators=[validate_opt_in_choice]
    )

    def __init__(self, data=None, do_third_party_auth=True):
        super(AccountCreationForm, self).__init__(data)
        self.extended_profile_fields = {}
        self.do_third_party_auth = do_third_party_auth

    def clean_password(self):
        """Enforce password policies (if applicable)"""
        password = self.cleaned_data["password"]
        if not self.do_third_party_auth:
            # Creating a temporary user object to test password against username
            # This user should NOT be saved
            username = self.cleaned_data.get('username')
            email = self.cleaned_data.get('email')
            temp_user = User(username=username, email=email) if username else None
            validate_password(password, temp_user)
        return password

    def clean_email(self):
        """ Enforce email restrictions (if applicable) """
        email = self.cleaned_data["email"]
        if settings.REGISTRATION_EMAIL_PATTERNS_ALLOWED is not None:
            # This Open edX instance has restrictions on what email addresses are allowed.
            allowed_patterns = settings.REGISTRATION_EMAIL_PATTERNS_ALLOWED
            # We append a '$' to the regexs to prevent the common mistake of using a
            # pattern like '.*@edx\\.org' which would match 'bob@edx.org.badguy.com'
            if not any(re.match(pattern + "$", email) for pattern in allowed_patterns):
                # This email is not on the whitelist of allowed emails. Check if
                # they may have been manually invited by an instructor and if not,
                # reject the registration.
                if not CourseEnrollmentAllowed.objects.filter(email=email).exists():
                    raise ValidationError(_("Unauthorized email address."))
        if email_exists_or_retired(email):
            raise ValidationError(
                _(
                    "It looks like {email} belongs to an existing account. Try again with a different email address."
                ).format(email=email)
            )
        return email

    def clean_org_name(self):
        """ Enforce organization related field conditions"""
        clean_org_name = self.cleaned_data.get("org_name")
        clean_org_size = self.cleaned_data.get("org_size")
        clean_org_type = self.cleaned_data.get("org_type")

        # User is affiliated with some organization
        if clean_org_name:
            # Check if organization already exists and does have a size populated
            existing_org = Organization.objects.filter(label=clean_org_name).first()

            if existing_org:
                existing_org_size = existing_org.total_employees
                if not existing_org_size and not clean_org_size:
                    raise forms.ValidationError(_("Organization size not provided for org with unpopulated size"))
                elif existing_org_size and clean_org_size:
                    raise forms.ValidationError(_("Organization size provided for existing org with populated size"))
            else:
                if not clean_org_size or not clean_org_type:
                    raise forms.ValidationError(_("Organization type/size not provided for a new org"))

        return clean_org_name


    @property
    def cleaned_extended_profile(self):
        """
        Return a dictionary containing the extended_profile_fields and values
        """
        return {
            key: value
            for key, value in self.cleaned_data.items()
            if key in self.extended_profile_fields and value is not None
        }

def get_registration_extension_form(*args, **kwargs):
    """
    Convenience function for getting the custom form set in settings.REGISTRATION_EXTENSION_FORM.

    An example form app for this can be found at http://github.com/open-craft/custom-form-app
    """
    if not settings.FEATURES.get("ENABLE_COMBINED_LOGIN_REGISTRATION"):
        return None
    if not getattr(settings, 'REGISTRATION_EXTENSION_FORM', None):
        return None
    module, klass = settings.REGISTRATION_EXTENSION_FORM.rsplit('.', 1)
    module = import_module(module)
    return getattr(module, klass)(*args, **kwargs)

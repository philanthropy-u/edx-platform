"""
Model form for the surveys.
"""
import json
import os
from datetime import datetime

from itertools import chain
from django import forms
from django.utils.encoding import force_unicode
from django.contrib.auth.models import User
from django.utils.translation import ugettext_noop
from rest_framework.compat import MinValueValidator, MaxValueValidator

from lms.djangoapps.onboarding.models import (
    UserExtendedProfile,
    Organization,
    OrganizationAdminHashKeys, EducationLevel, EnglishProficiency, RoleInsideOrg, OperationLevel,
    FocusArea, TotalEmployee, OrgSector)
from lms.djangoapps.onboarding.email_utils import send_admin_activation_email


NO_OPTION_SELECT_ERROR = 'Please select an option for {}'
EMPTY_FIELD_ERROR = 'Please enter your {}'


def get_onboarding_autosuggesion_data(file_name):
    """
    Receives a json file name and return data related to autocomplete fields in
    onboarding survey.
    """

    curr_dir = os.path.dirname(__file__)
    file_path = "{}/{}".format('data', file_name)
    json_file = open(os.path.join(curr_dir, file_path))
    data = json.load(json_file)
    return data


def is_selected_from_autocomplete(autocomplete_data, submitted_input):
    """
    Checks whether submitted input lies in autocomplete data or not.
    """

    for value in autocomplete_data:
        if value == submitted_input:
            return True
    return False


class UserInfoModelForm(forms.ModelForm):
    """
    Model from to be used in the first step of survey.

    This will record some basic information about the user as modeled in
    'UserInfoSurvey' model
    """
    GENDER_CHOICES = (
        ('m', ugettext_noop('Male')),
        ('f', ugettext_noop('Female')),
        # Translators: 'Other' refers to the student's gender
        ('o', ugettext_noop("I'd rather not say")),
        ('nl', ugettext_noop('Not listed')),
    )

    NO_SELECT_CHOICE = [('', '- Select -')]

    LEVEL_OF_EDUCAION_CHOICES = NO_SELECT_CHOICE  + [(el.code, el.label) for el in EducationLevel.objects.all()]
    ENLISHP_ROFICIENCY_CHOICES = NO_SELECT_CHOICE + [(ep.code, ep.label) for ep in EnglishProficiency.objects.all()]
    ROLE_IN_ORG_CHOICES = NO_SELECT_CHOICE + [(r.code, r.label) for r in RoleInsideOrg.objects.all()]

    year_of_birth = forms.IntegerField(
        label="Year of Birth",
        label_suffix="*",
        validators=[
            MinValueValidator(1900, message='Ensure year of birth is greater than or equal to 1900'),
            MaxValueValidator(
                datetime.now().year, message='Ensure year of birth is less than or equal to {}'.format(
                    datetime.now().year
                )
            )
        ],
        error_messages={
            'required': EMPTY_FIELD_ERROR.format("Year of birth"),
        }
    )
    gender = forms.ChoiceField(label='Gender', required=False, label_suffix="*", choices=GENDER_CHOICES,
                               widget=forms.RadioSelect)

    language = forms.CharField(label="Native Language", label_suffix="*", required=True,
                               error_messages={"required": EMPTY_FIELD_ERROR.format('Language')})
    country = forms.CharField(label="Country of Residence", label_suffix="*",
                              error_messages={"required": EMPTY_FIELD_ERROR.format("Country of Residence")
    })
    city = forms.CharField(label="City of Residence", required=False)
    is_emp_location_different = forms.BooleanField(label='Check here if your country and/or city of employment is '
                                                         'different from your country and/or city of residence.',
                                                   required=False)
    level_of_education = forms.ChoiceField(label="Level of Education", label_suffix="*",
                                           choices=LEVEL_OF_EDUCAION_CHOICES,
                                           error_messages={
                                                'required': NO_OPTION_SELECT_ERROR.format(
                                                    'Level of Education'),
                                           })
    english_proficiency = forms.ChoiceField(label="English Language Proficiency", label_suffix="*",
                                            choices=ENLISHP_ROFICIENCY_CHOICES,
                                            error_messages={
                                                 'required': NO_OPTION_SELECT_ERROR.format(
                                                     'English Language Proficiency'),
                                            })
    role_in_org = forms.ChoiceField(label="Role in the Organization",
                                    label_suffix="*",
                                    choices=ROLE_IN_ORG_CHOICES,
                                    error_messages={
                                         'required': NO_OPTION_SELECT_ERROR.format(
                                             'Role in the Organization'),
                                    })

    def __init__(self,  *args, **kwargs):
        super(UserInfoModelForm, self).__init__( *args, **kwargs)

        FUNCTION_AREA_CHOICS = ((field_name, label) for field_name, label in
                                UserExtendedProfile.FUNCTIONS_LABELS.items())
        self.fields['function_areas'] = forms.ChoiceField(choices=FUNCTION_AREA_CHOICS,
            label='Department of Function (Check all that apply.)',
            widget=forms.CheckboxSelectMultiple)


    def clean(self):
        if self.errors.get('function_areas'):
            del self.errors['function_areas']

    def clean_gender(self):

        not_listed_gender = self.data.get('not_listed_gender', None)
        gender = self.cleaned_data['gender']

        if not gender:
            raise forms.ValidationError('Please select Gender.')

        if gender == 'nl' and not not_listed_gender:
            raise forms.ValidationError('Please specify Gender.')

        return gender

    def clean_country(self):

        all_countries = get_onboarding_autosuggesion_data('world_countries.json')
        country = self.cleaned_data['country']

        if is_selected_from_autocomplete(all_countries, country):
            return country

        raise forms.ValidationError('Please select country of residence.')

    def clean_language(self):

        all_languages = get_onboarding_autosuggesion_data('world_languages.json')
        submitted_language = self.cleaned_data['language']

        if is_selected_from_autocomplete(all_languages, submitted_language):
            return submitted_language

        raise forms.ValidationError('Please select language.')

    class Meta:
        """
        The meta class used to customize the default behaviour of form fields
        """
        model = UserExtendedProfile
        fields = [
            'year_of_birth', 'gender', 'not_listed_gender', 'not_listed_gender', 'level_of_education', 'language',
            'english_proficiency', 'country', 'city', 'is_emp_location_different', 'role_in_org', 'start_month_year',
            'hours_per_week'
        ]

        labels = {
            'is_emp_location_different': 'Check here if your country and/or city of employment is different'
                                         ' from your country and/or city of residence.',
            'start_month_year': "Start Month and Year*",
            'role_in_org': 'Role in Organization*',
        }
        widgets = {
            'year_of_birth': forms.TextInput,
            'country': forms.TextInput,
            'not_listed_gender': forms.TextInput(attrs={'placeholder': 'Identify your gender here'}),
            'city': forms.TextInput,
            'language': forms.TextInput,
            'start_month_year': forms.TextInput(attrs={'placeholder': 'mm/yy'}),
        }

        error_messages = {
            "hours_per_week": {
                'required': EMPTY_FIELD_ERROR.format('Typical Number of Hours Worked per Week')
            },
            'start_month_year': {
                'required': EMPTY_FIELD_ERROR.format('Start Month and Year'),
            }
        }

    def save(self, request, commit=True):
        user_info_survey = super(UserInfoModelForm, self).save()

        userprofile = user_info_survey.user.profile
        userprofile.year_of_birth = self.cleaned_data['year_of_birth']
        userprofile.language = self.cleaned_data['language']
        userprofile.country = self.cleaned_data['country']
        userprofile.city = self.cleaned_data['city']
        if self.cleaned_data['gender']:
            userprofile.gender = self.cleaned_data['gender']
        userprofile.save()

        user_info_survey.user.extended_profile.save_user_function_areas(request.POST.getlist('function_areas'))
        if commit:
            user_info_survey.save()

        return user_info_survey


class RadioSelectNotNull(forms.RadioSelect):
    """
    A widget which removes the default '-----' option from RadioSelect
    """
    def get_renderer(self, name, value, attrs=None, choices=()):
        """
        Returns an instance of the renderer.
        """
        if value is None: value = ''
        # Normalize to string.
        str_value = force_unicode(value)
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        if choices[0][0] == '':
            choices.pop(0)
        return self.renderer(name, str_value, final_attrs, choices)


class InterestsForm(forms.Form):
    """
    Model from to be used in the second step of survey.

    This will record user's interests information as modeled in
    'InterestsSurvey' model.
    """

    def __init__(self,  *args, **kwargs):
        super(InterestsForm, self).__init__( *args, **kwargs)
        INTEREST_CHOICS = ((field_name, label) for field_name, label in UserExtendedProfile.INTERESTS_LABELS.items())
        self.fields['interests'] = forms.ChoiceField(
            label='Which of these areas of organizational effectiveness are you most interested '
                  'to learn more about? (Check all that apply)',
            choices=INTEREST_CHOICS, widget=forms.CheckboxSelectMultiple,
            required=False)

        INTERESTED_LEARNERS_CHOICS = ((field_name, label)
                                for field_name, label in UserExtendedProfile.INTERESTED_LEARNERS_LABELS.items())
        self.fields['interested_learners'] = forms.ChoiceField(
            label='Which type of other Philanthropy University learners are interesting to you? (Check all that apply)',
            choices=INTERESTED_LEARNERS_CHOICS, widget=forms.CheckboxSelectMultiple,
            required=False)

        PERSONAL_GOAL_CHOICS = ((field_name, label) for field_name, label in UserExtendedProfile.GOALS_LABELS.items())
        self.fields['personal_goals'] = forms.ChoiceField(
            label='What is your most important personal goals in joining Philanthropy University? (Check all that apply)',
            choices=PERSONAL_GOAL_CHOICS, widget=forms.CheckboxSelectMultiple,
            required=False)

    def save(self, request, user_exended_profile):
        user_exended_profile.save_user_interests(request.POST.getlist('interests'))
        user_exended_profile.save_user_interested_learners(request.POST.getlist('interested_learners'))
        user_exended_profile.save_user_personal_goals(request.POST.getlist('personal_goals'))

        user_exended_profile.save()


class OrganizationInfoForm(forms.ModelForm):
    """
    Model from to be used in the third step of survey.

    This will record information about user's organization as modeled in
    'OrganizationSurvey' model.
    """
    is_org_url_exist = forms.ChoiceField(label="Does your organization have a website?",
                                         label_suffix="*",
                                         widget=forms.RadioSelect(choices=((0, "Yes"), (1, "No"))),
                                         initial=1,
                                         error_messages={
                                            'required': 'Please select an option for "Does your organization have a'
                                                        ' webpage?"',
                                         })

    org_type = forms.ChoiceField(label="Organization Type", label_suffix="*",
                                 choices=((os.code, os.label) for os in OrgSector.objects.all()),
                                 error_messages={
                                     'required': NO_OPTION_SELECT_ERROR.format(
                                         'Organization Type'),
                                 })

    level_of_operation = forms.ChoiceField(label="Level of Operation", label_suffix="*",
                                           choices=((ol.code, ol.label) for ol in OperationLevel.objects.all()),
                                           error_messages={
                                               'required': NO_OPTION_SELECT_ERROR.format(
                                                   'Level of Operation'),
                                           })

    focus_area = forms.ChoiceField(label="Primary Focus Area", label_suffix="*",
                                   choices=((fa.code, fa.label) for fa in FocusArea.objects.all()),
                                   error_messages={
                                       'required': NO_OPTION_SELECT_ERROR.format(
                                           'Primary Focus Areas'),
                                   })

    total_employees = forms.ChoiceField(label="Total Employees", label_suffix="*",
                                        choices=((ep.code, ep.label) for ep in TotalEmployee.objects.all()),
                                        error_messages={
                                            'required': NO_OPTION_SELECT_ERROR.format('Total Employees'),
                                        })

    def __init__(self,  *args, **kwargs):
        super(OrganizationInfoForm, self).__init__( *args, **kwargs)
        self.fields['level_of_operation'].empty_label = "- Select -"
        self.fields['focus_area'].empty_label = "- Select -"
        self.fields['total_employees'].empty_label = "- Select -"
        self.fields['org_type'].empty_label = "- Select -"

    class Meta:
        """
        The meta class used to customize the default behaviour of form fields
        """
        model = Organization
        fields = ['country', 'city', 'is_org_url_exist', 'url', 'founding_year', 'org_type', 'level_of_operation',
                  'focus_area', 'total_employees', 'alternate_admin_email']

        widgets = {
            'country': forms.TextInput,
            'city': forms.TextInput,
            'url': forms.TextInput,
            'founding_year': forms.NumberInput,
            'alternate_admin_email': forms.TextInput,
        }

        labels = {
            'country': "Country of Organization Headquarters*",
            'city': "City of Organization Headquarters*",
            'is_org_url_exist': "Does your organization have a webpage?",
            'url': "Website Address*",
            'alternate_admin_email': 'Primary Focus Area*',
        }

        required_error = 'Please select an option for {}'

        error_messages = {
            'founding_year': {
                'required': required_error.format('Founding Year'),
            },
            'country': {
                'required': EMPTY_FIELD_ERROR.format('Country of Organization Headquarters'),
            }
        }

    def clean_country(self):

        all_countries = get_onboarding_autosuggesion_data('world_countries.json')
        country = self.cleaned_data['country']

        if is_selected_from_autocomplete(all_countries, country):
            return country

        raise forms.ValidationError('Please select country of Organization Headquarters.')
#
    def clean_url(self):
        is_org_url_exist = int(self.data.get('is_org_url_exist')) if self.data.get('is_org_url_exist') else None
        organization_website = self.cleaned_data['url']

        if is_org_url_exist and not organization_website:
            raise forms.ValidationError(EMPTY_FIELD_ERROR.format('Organization Website'))

        return organization_website

    def clean(self):
        """
        Clean the form after submission and ensure that year is 4 digit positive number.
        """
        cleaned_data = super(OrganizationInfoForm, self).clean()

        year = cleaned_data['founding_year']

        if year:
            if len("{}".format(year)) < 4 or year < 0 or len("{}".format(year)) > 4:
                self.add_error(
                    'founding_year',
                    "You entered an invalid year format. Please enter a valid year with 4 digits."
                )


class RegModelForm(forms.ModelForm):
    """
    Model form for extra fields in registration model
    """

    IS_POC_CHOICES = (
        (1, 'Yes'),
        (0, 'No')
    )

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'First Name'}
        )
    )

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={'placeholder': 'Last Name'}
        )
    )

    organization_name = forms.CharField(
        max_length=255,
        label='Organization Name',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Organization Name'}
        ),
        initial='Organization Name'
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        initial='Confirm Password'
    )

    is_currently_employed = forms.BooleanField(
        initial=False,
        required=False,
        label="Check here if you are currently unemployed or otherwise not affiliated with an organization."
    )

    is_poc = forms.ChoiceField(label='Are you the Admin of your organization?',
                               choices=IS_POC_CHOICES,
                               widget=forms.RadioSelect)

    org_admin_email = forms.CharField(required=False,
                                      widget=forms.EmailInput(attrs=({'placeholder': 'Organization Admin Email'})))

    def __init__(self, *args, **kwargs):
        super(RegModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = 'First Name'
        self.fields['last_name'].initial = 'Last Name'
        self.fields['org_admin_email'].initial = 'Organization Admin Email'

        self.fields['first_name'].error_messages = {
            'required': 'Please enter your First Name.',
        }

        self.fields['last_name'].error_messages = {
            'required': 'Please enter your Last Name.',
        }

        self.fields['organization_name'].error_messages = {
            'required': 'Please select your Organization.',
        }

        self.fields['confirm_password'].error_messages = {
            'required': 'Please enter your Confirm Password.',
        }

    class Meta:
        model = UserExtendedProfile

        fields = (
            'confirm_password', 'first_name', 'last_name',
            'organization_name', 'is_currently_employed', 'is_poc', 'org_admin_email',
        )

        labels = {
            'org_admin_email': 'If you know who should be the Admin for [Organization name],'
                               ' please provide their email address and we will invite them to sign up.',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'org_admin_email': forms.EmailInput(attrs=({'placeholder': 'Organization Admin Email'}))
        }

        serialization_options = {
            'confirm_password': {'field_type': 'password'},
            'org_admin_email': {'field_type': 'email'}
        }


    def clean_organization_name(self):
        organization_name = self.cleaned_data['organization_name']

        if not self.data.get('is_currently_employed') and not organization_name:
            raise forms.ValidationError("Please enter organization name")

        return organization_name

    def save(self, user=None, commit=True):
        prev_org = None

        organization_name = self.cleaned_data['organization_name']
        is_poc = self.cleaned_data['is_poc']
        org_admin_email = self.cleaned_data['org_admin_email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        organization_to_assign, is_created = Organization.objects.get_or_create(label=organization_name)
        extended_profile, is_profile_created = UserExtendedProfile.objects.get_or_create(user=user)
        user_obj = extended_profile.user

        if not is_profile_created:
            prev_org = extended_profile.organization

        if user and is_poc == '1':
            organization_to_assign.admin = user
            organization_to_assign.save()

        if prev_org:
            if organization_to_assign.lable != prev_org.label:
                prev_org.admin = None
                prev_org.save()

        extended_profile.organization = organization_to_assign
        user_obj.first_name = first_name
        user_obj.last_name = last_name

        if org_admin_email:
            try:
                User.objects.get(email=org_admin_email)

                hash_key = OrganizationAdminHashKeys.assign_hash(organization_to_assign, user, org_admin_email)
                org_id = extended_profile.organization_id
                org_name = extended_profile.organization.label

                send_admin_activation_email(org_id, org_name, org_admin_email, user, hash_key)
            except User.DoesNotExist:
                pass
            except Exception:
                pass

        user.save()

        if commit:
            extended_profile.save()

        return extended_profile


class UpdateRegModelForm(RegModelForm):
    """
    Model form to update the registration extra fields
    """
    def __init__(self, *args, **kwargs):
        super(UpdateRegModelForm, self).__init__(*args, **kwargs)
        self.fields.pop('confirm_password')


class OrganizationDetailModelForm(forms.ModelForm):

    currency_input = forms.CharField(
        max_length=255,
        label='Local currency code*',
        widget=forms.TextInput(
            attrs={'placeholder': 'Local currency code*'}
        ),
        required=False
    )

    # def __init__(self,  *args, **kwargs):
    #     super(OrganizationDetailModelForm, self).__init__(*args, **kwargs)
    #     self.fields['can_provide_info'].empty_label = None
    #     self.fields['info_accuracy'].empty_label = None
    #     self.fields['can_provide_info'].required = True
    #
    #     self.fields['info_accuracy'].required = False
    #     self.fields['last_fiscal_year_end_date'].required = False
    #     self.fields['total_clients'].required = False
    #     self.fields['total_employees'].required = False
    #     self.fields['currency_input'].required = False
    #     self.fields['total_revenue'].required = False
    #     self.fields['total_expenses'].required = False
    #     self.fields['total_program_expenses'].required = False
    #
    # class Meta:
    #     model = OrganizationDetailSurvey
    #
    #     fields = [
    #         'can_provide_info', 'info_accuracy', 'last_fiscal_year_end_date', 'total_clients',
    #         'total_employees', 'currency_input', 'total_revenue', 'total_expenses', 'total_program_expenses'
    #     ]
    #
    #
    #     widgets = {
    #         'can_provide_info': forms.RadioSelect,
    #         'info_accuracy': RadioSelectNotNull,
    #         'last_fiscal_year_end_date': forms.TextInput(attrs={'placeholder': 'End Date of Last Fiscal Year*'}),
    #         'total_clients': forms.NumberInput(
    #             attrs={'placeholder': 'Total Annual Clients or Direct Beneficiaries for Last Fiscal Year*'}
    #         ),
    #         'total_employees': forms.NumberInput(attrs={'placeholder': 'Total Employees at End of Last Fiscal Year*'}),
    #
    #         'total_revenue': forms.NumberInput(
    #             attrs={'placeholder': 'Total Annual Revenue for Last Fiscal Year (local currency)*'}
    #         ),
    #         'total_expenses': forms.NumberInput(
    #             attrs={'placeholder': 'Total Annual Expenses for Last Fiscal Year (local currency)*'}
    #         ),
    #         'total_program_expenses': forms.NumberInput(
    #             attrs={'placeholder': 'Total Annual Program Expenses for Last Fiscal Year (local currency)*'}
    #         )
    #     }
    #
    #     labels = {
    #         'can_provide_info': 'Are you able to provide the information requested below?',
    #         'info_accuracy': 'Is the information you will provide on this page estimated or actual?'
    #     }
    #
    #     help_texts = {
    #         'last_fiscal_year_end_date': "If the data you are providing below is for the last 12 months,"
    #                                      " please enter today's date."
    #     }
    #
    #     error_messages = {
    #         'can_provide_info': {
    #             'required': "Please select an option for providing information.",
    #         },
    #     }
    #
    # def clean_currency_input(self):
    #     can_provide_info = int(self.data['can_provide_info']) if self.data.get('can_provide_info') else False
    #     all_currency_codes = Currency.objects.values_list('alphabetic_code', flat=True)
    #     currency_input = self.cleaned_data['currency_input']
    #
    #     if can_provide_info and not is_selected_from_autocomplete(all_currency_codes, currency_input):
    #         raise forms.ValidationError('Please select currency code.')
    #
    #     return currency_input
    #
    #
    # def clean_info_accuracy(self):
    #     can_provide_info = int(self.data['can_provide_info']) if self.data.get('can_provide_info') else False
    #     info_accuracy = self.cleaned_data['info_accuracy']
    #
    #     if can_provide_info and info_accuracy not in [True, False]:
    #         raise forms.ValidationError("Please select an option for Estimated or Actual Information")
    #
    #     return info_accuracy
    #
    # def clean_last_fiscal_year_end_date(self):
    #     can_provide_info = int(self.data.get('can_provide_info')) if self.data.get('can_provide_info') else False
    #     last_fiscal_year_end_date = self.cleaned_data['last_fiscal_year_end_date']
    #
    #     if can_provide_info and not last_fiscal_year_end_date:
    #         raise forms.ValidationError(EMPTY_FIELD_ERROR.format("End date for Last Fiscal Year"))
    #
    #     return last_fiscal_year_end_date
    #
    # def clean_total_clients(self):
    #     can_provide_info = int(self.data.get('can_provide_info')) if self.data.get('can_provide_info') else False
    #     total_clients = self.cleaned_data['total_clients']
    #
    #     if can_provide_info and not total_clients:
    #         raise forms.ValidationError(EMPTY_FIELD_ERROR.format("Total Client"))
    #
    #     return total_clients
    #
    # def clean_total_employees(self):
    #     can_provide_info = int(self.data.get('can_provide_info')) if self.data.get('can_provide_info') else False
    #     total_employees = self.cleaned_data['total_employees']
    #
    #     if can_provide_info and not total_employees:
    #         raise forms.ValidationError(EMPTY_FIELD_ERROR.format("Total Employees"))
    #
    #     return total_employees
    #
    # def clean_total_revenue(self):
    #     can_provide_info = int(self.data.get('can_provide_info')) if self.data.get('can_provide_info') else False
    #     total_revenue = self.cleaned_data['total_revenue']
    #
    #     if can_provide_info and not total_revenue:
    #         raise forms.ValidationError(EMPTY_FIELD_ERROR.format("Total Revenue"))
    #
    #     return total_revenue
    #
    # def clean_total_expenses(self):
    #     can_provide_info = int(self.data.get('can_provide_info')) if self.data.get('can_provide_info') else False
    #     total_expenses = self.cleaned_data['total_expenses']
    #
    #     if can_provide_info and not total_expenses:
    #         raise forms.ValidationError(EMPTY_FIELD_ERROR.format("Total Expenses"))
    #
    #     return total_expenses
    #
    # def clean_total_program_expenses(self):
    #     can_provide_info = int(self.data.get('can_provide_info')) if self.data.get('can_provide_info') else False
    #     total_program_expenses = self.cleaned_data['total_program_expenses']
    #
    #     if can_provide_info and not total_program_expenses:
    #         raise forms.ValidationError(EMPTY_FIELD_ERROR.format("Total Program Expense"))
    #
    #     return total_program_expenses
    #
    #
    # def save(self, user=None, commit=True):
    #     org_detail = super(OrganizationDetailModelForm, self).save(commit=False)
    #     if user:
    #         org_detail.user = user
    #
    #     can_provide_info = int(self.data['can_provide_info'])
    #     if can_provide_info:
    #         org_detail.currency = Currency.objects.filter(alphabetic_code=self.cleaned_data['currency_input']).first()
    #
    #     if commit:
    #         org_detail.save()
    #
    #     return org_detail
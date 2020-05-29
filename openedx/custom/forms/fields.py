from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectFormField

from openedx.custom.helpers import add_other_field_in_choices, get_other_values
from openedx.custom.forms.widgets import CheckboxSelectMultipleWithOther, RadioSelectWithOther


class MultiSelectWithOtherFormField(MultiSelectFormField):
    """
    Form field class to handle other text input field within the multiselect field
    """

    def __init__(self, other_max_length=None, is_other_custom=False, *args, **kwargs):
        if kwargs.get('choices'):
            kwargs['choices'] = add_other_field_in_choices(kwargs['choices'])

        self.widget = CheckboxSelectMultipleWithOther(is_other_custom)
        # self.widget = CheckboxSelectMultipleWithOther()

        if kwargs.get('max_choices') == 1:
            self.widget = RadioSelectWithOther(is_other_custom)
            # self.widget.input_type = 'radio'
            # self.widget.template_name = 'django/forms/widgets/radio.html'
            # self.widget.option_template_name = 'django/forms/widgets/radio_option.html'

        super(MultiSelectWithOtherFormField, self).__init__(*args, **kwargs)

        self.other_max_length = other_max_length
        self.error_messages.update(
            dict(invalid_length=_(
                'Other field value, maximum allowed length violation. Allowed limit is upto {other_max_length}'
                ' characters.').format(
                other_max_length=other_max_length)))

    def valid_value(self, value):
        return len(value) <= self.other_max_length

    def validate(self, value):
        """
        Validate that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')

        if self.other_max_length is not None:
            other_values = get_other_values(self.choices, value)
            for val in other_values:
                if not self.valid_value(val):
                    raise ValidationError(
                        self.error_messages['invalid_length'],
                        code='invalid_length',
                        params={'value': val},
                    )

    def clean(self, value):
        value = [val for val in value if val not in self.empty_values]
        return super(MultiSelectWithOtherFormField, self).clean(value)

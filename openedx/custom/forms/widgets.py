from django.forms.widgets import CheckboxSelectMultiple

from openedx.custom.helpers import get_other_values


class CheckboxSelectMultipleWithOther(CheckboxSelectMultiple):
    """
    Widget class to handle other value filed.
    """

    def __init__(self, is_other_custom):
        super(CheckboxSelectMultipleWithOther, self).__init__()

        self.other_choice = None
        self.is_other_custom = is_other_custom

        # if is_other_custom:
        #     self.other_option_template_name = 'custom.html'
        # else:
        #     self.other_option_template_name = 'django/forms/widgets/text.html'

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(CheckboxSelectMultipleWithOther, self).create_option(name, value, label, selected, index,
                                                                            subindex, attrs)
        if value == 'other':
            if self.other_choice == '':
                selected = False
            else:
                selected = True
            option.update({
                'value': self.other_choice,
                'selected': selected,
                'type': 'text' if not self.is_other_custom else option['type'],
                'template_name': 'django/forms/widgets/text.html' if not self.is_other_custom else 'custom.html',
                'is_other': True
            })

        return option

    def optgroups(self, name, value, attrs=None):
        """
        Return a list of optgroups for this widget.
        """

        other_values = get_other_values(self.choices, value)

        OTHER_CHOICE_INDEX = 0
        other_values = '' if not other_values else other_values.pop(OTHER_CHOICE_INDEX)

        self.other_choice = other_values

        return super(CheckboxSelectMultipleWithOther, self).optgroups(name, value, attrs)


class RadioSelectWithOther(CheckboxSelectMultipleWithOther):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(RadioSelectWithOther, self).create_option(name, value, label, selected, index, subindex, attrs)

        option.update({
            'type': 'radio'
        })

        if value != 'other':
            option['attrs']['onclick'] = "document.getElementById('id_other').disabled=true;"

        return option

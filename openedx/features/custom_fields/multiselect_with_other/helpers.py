"""All helpers for custom_fields app"""

from openedx.features.custom_fields.multiselect_with_other.constants import OTHER_FIELD_CHECKBOX_VALUE


def add_other_field_in_choices(choices):
    """
    This adds other option in multi select choices
    :param choices: list of choices
    :type choices: list
    :return: list, dict or tuple with other field.
    :rtype: list, dict or tuple
    """
    _choices = choices

    if isinstance(_choices, dict):
        _choices = _choices.items()

    if 'other' not in [c for c, _ in _choices]:
        if isinstance(choices, tuple):
            return choices + (('other', 'Other'),)
        if isinstance(choices, list):
            return choices + [('other', 'Other')]
        if isinstance(choices, dict):
            choices['other'] = 'Other'
            return choices

    return choices


def get_other_values(choices, value):
    """
    This function to separate other's value from list of choices
    :param choices: list of valid choices
    :param value: list of selected choices including other's value
    :type choices: list
    :type value: list
    :return: list, dict or tuple with other field.
    :rtype: list, dict or tuple
    """
    choice_values = [choice[0] for choice in choices]
    other_values = [val for val in value if val not in choice_values]
    return other_values


def filter_other_field_checkbox_value(values):
    """
    This function filters for the value that is automatically put
    into the form payload when other field is selected in usage of
    MultiSelectWithOtherField
    :param values: list of strings
    :type values: list
    :return: list of strings with the OTHER_FIELD_CHECKBOX_VALUE removed
    :rtype: list
    """
    if isinstance(values, list) and OTHER_FIELD_CHECKBOX_VALUE in values:
        values.remove(OTHER_FIELD_CHECKBOX_VALUE)

    return values

"""Defines serializers used by the Team API."""
from lms.djangoapps.teams.serializers import CourseTeamCreationSerializer, CountryField
from rest_framework import serializers
from django.conf import settings


class PhiluTeamsCountryField(CountryField):
    """
    Field to serialize a country code.
    """

    def to_internal_value(self, data):
        """
        Check that the code is a valid country code.

        We leave the data in its original format so that the Django model's
        CountryField can convert it to the internal representation used
        by the django-countries library.
        """

        if not data:
            raise serializers.ValidationError(
                "Country field is required"
            )

        if data and data not in self.COUNTRY_CODES:
            raise serializers.ValidationError(
                u"{code} is not a valid country code".format(code=data)
            )
        return data


class PhiluTeamsLanguageField(serializers.Field):
    """
    Field to serialize a Language code.
    """

    LANGUAGE_CODES = dict(settings.ALL_LANGUAGES).keys()

    def to_representation(self, obj):
        """
        Represent the country as a 2-character unicode identifier.
        """
        return unicode(obj)

    def to_internal_value(self, data):
        """
        Check that the code is a valid language code.

        We leave the data in its original format so that the Django model's
        CountryField can convert it to the internal representation used
        by the django-countries library.
        """

        if not data:
            raise serializers.ValidationError(
                "Language field is required"
            )

        if data and data not in self.LANGUAGE_CODES:
            raise serializers.ValidationError(
                u"{code} is not a valid language code".format(code=data)
            )
        return data


class PhiluTeamsCourseTeamCreationSerializer(CourseTeamCreationSerializer):
    country = PhiluTeamsCountryField(required=True)
    language = PhiluTeamsLanguageField(required=True)

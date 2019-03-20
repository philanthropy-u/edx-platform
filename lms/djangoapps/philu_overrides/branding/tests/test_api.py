# encoding: utf-8
"""Tests of Branding API """
from __future__ import unicode_literals

import mock
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from ..api import get_logo_url, get_auth_footer, get_non_auth_footer, get_about_url, get_privacy_url, get_tos_and_honor_code_url


class TestHeader(TestCase):
    """Test API end-point for retrieving the header. """

    def test_cdn_urls_for_logo(self):
        # Ordinarily, we'd use `override_settings()` to override STATIC_URL,
        # which is what the staticfiles storage backend is using to construct the URL.
        # Unfortunately, other parts of the system are caching this value on module
        # load, which can cause other tests to fail.  To ensure that this change
        # doesn't affect other tests, we patch the `url()` method directly instead.
        cdn_url = "http://cdn.example.com/static/image.png"
        with mock.patch('branding.api.staticfiles_storage.url', return_value=cdn_url):
            logo_url = get_logo_url()

        self.assertEqual(logo_url, cdn_url)


class TestFooter(TestCase):
    """Test retrieving the footer. """

    @mock.patch.dict('django.conf.settings.FEATURES', {'ENABLE_MKTG_SITE': True})
    @mock.patch.dict('django.conf.settings.MKTG_URLS', {
        "ROOT": "https://philanthropyu.org",
        "ABOUT": "/about-us/our-story/",
        "TOS_AND_HONOR": "/terms-of-use/",
        "PRIVACY": "/privacy-policy/"
    })
    @override_settings(PLATFORM_NAME='\xe9dX')
    def test_get_auth_footer(self):
        actual_auth_footer = get_auth_footer()

        expected_footer = {
            'copyright': '\xa9 \xe9dX.  All rights reserved except where noted.  EdX, Open edX and the edX and Open'
                         ' EdX logos are registered trademarks or trademarks of edX Inc.',
            'navigation_links': [
                {
                    "name": "about",
                    "target": "_blank",
                    "title": "About Philanthropy University",
                    "url": get_about_url()
                }
            ],
            'legal_links': [
                {
                    "name": "terms_of_service_and_honor_code",
                    "target": "_blank",
                    "title": "Terms of Use",
                    "url": get_tos_and_honor_code_url()
                },
                {
                    "name": "privacy_policy",
                    "target": "_blank",
                    "title": "Privacy Policy",
                    "url": get_privacy_url()
                },
                {
                    "name": "faq",
                    "target": "_blank",
                    "title": "FAQ",
                    "url": "https://philanthropyu.org/faq/"
                }
            ],
            'social_links': [
                {
                    "action": "Follow \xe9dX on LinkedIn",
                    "icon-class": "fa-linkedin",
                    "name": "linkedin",
                    "title": "LinkedIn",
                    "url": "#"
                },
                {
                    "action": "Like \xe9dX on Facebook",
                    "icon-class": "fa-facebook",
                    "name": "facebook",
                    "title": "Facebook",
                    "url": "#"
                },
                {
                    "action": "Follow \xe9dX on Twitter",
                    "icon-class": "fa-twitter",
                    "name": "twitter",
                    "title": "Twitter",
                    "url": "#"
                },
                {
                    "action": "Subscribe to the \xe9dX YouTube channel",
                    "icon-class": "fa-youtube",
                    "name": "youtube",
                    "title": "Youtube",
                    "url": "#"
                }

            ],
            "courses_communities_links": [
                {
                    "class": "",
                    "name": "explore_course",
                    "target": "_self",
                    "title": "Explore our Courses",
                    "url": "/courses"
                },
                {
                    "class": "communities-link",
                    "name": "communities",
                    "target": "_self",
                    "title": "Be part of our Communities",
                    "url": settings.NODEBB_ENDPOINT
                }
            ],

        }

        self.assertEqual(actual_auth_footer, expected_footer)

    @mock.patch.dict('django.conf.settings.FEATURES', {'ENABLE_MKTG_SITE': True})
    @mock.patch.dict('django.conf.settings.MKTG_URLS', {
        "ROOT": "https://philanthropyu.org",
        "ABOUT": "/about-us/our-story/",
        "TOS_AND_HONOR": "/terms-of-use/",
        "PRIVACY": "/privacy-policy/"
    })
    @override_settings(PLATFORM_NAME='\xe9dX')
    def test_get_non_auth_footer(self):
        actual_footer = get_non_auth_footer()

        expected_footer = {
            'copyright': '\xa9 \xe9dX.  All rights reserved except where noted.  EdX, Open edX and the edX and Open'
                         ' EdX logos are registered trademarks or trademarks of edX Inc.',
            'navigation_links': [
                {
                    "name": "about",
                    "target": "_blank",
                    "title": "About Philanthropy University",
                    "url": get_about_url()
                },
                {
                    "name": "explore_course",
                    "target": "_self",
                    "title": "Explore our Courses",
                    "url": "/courses"
                },
                {
                    "name": "communities",
                    "target": "_self",
                    "title": "Be part of our Communities",
                    "url": settings.NODEBB_ENDPOINT
                }
            ],
            'legal_links': [
                {
                    "name": "terms_of_service_and_honor_code",
                    "target": "_blank",
                    "title": "Terms of Use",
                    "url": get_tos_and_honor_code_url()
                },
                {
                    "name": "privacy_policy",
                    "target": "_blank",
                    "title": "Privacy Policy",
                    "url": get_privacy_url()
                },
                {
                    "name": "faq",
                    "target": "_blank",
                    "title": "FAQ",
                    "url": "https://philanthropyu.org/faq/"
                }
            ],
            'social_links': [
                {
                    "action": "Follow \xe9dX on LinkedIn",
                    "icon-class": "fa-linkedin",
                    "name": "linkedin",
                    "title": "LinkedIn",
                    "url": "#"
                },
                {
                    "action": "Like \xe9dX on Facebook",
                    "icon-class": "fa-facebook",
                    "name": "facebook",
                    "title": "Facebook",
                    "url": "#"
                },
                {
                    "action": "Follow \xe9dX on Twitter",
                    "icon-class": "fa-twitter",
                    "name": "twitter",
                    "title": "Twitter",
                    "url": "#"
                },
                {
                    "action": "Subscribe to the \xe9dX YouTube channel",
                    "icon-class": "fa-youtube",
                    "name": "youtube",
                    "title": "Youtube",
                    "url": "#"
                }

            ]
        }

        self.assertEqual(actual_footer, expected_footer)

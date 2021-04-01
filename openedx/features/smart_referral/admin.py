# -*- coding: utf-8 -*-
"""
Admin configurations for smart_referral app
"""
from __future__ import unicode_literals

from django.contrib import admin

from .models import SmartReferral


class SmartReferralAdmin(admin.ModelAdmin):
    """
    Django admin customizations for SmartReferral model.
    """

    list_display = ('user', 'contact_email')
    search_fields = ('user__username', 'contact_email')
    raw_id_fields = ('user', )


admin.site.register(SmartReferral, SmartReferralAdmin)

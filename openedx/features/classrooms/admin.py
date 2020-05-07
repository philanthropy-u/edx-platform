from django.contrib import admin

from models import DiscussionCommunityMembership


class DiscussionCommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'community')


admin.site.register(DiscussionCommunityMembership, DiscussionCommunityMembershipAdmin)

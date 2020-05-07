from django.contrib import admin

from models import DiscussionCommunity, DiscussionCommunityMembership


class DiscussionCommunityAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'community_url')


class DiscussionCommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'community')


admin.site.register(DiscussionCommunity, DiscussionCommunityAdmin)
admin.site.register(DiscussionCommunityMembership, DiscussionCommunityMembershipAdmin)

from django.contrib import admin

from models import DiscussionCommunity, DiscussionCommunityMembership, DiscussionCommunityThrough


class DiscussionCommunityAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'community_url')


class DiscussionCommunityInline(admin.TabularInline):
    model = DiscussionCommunityThrough


class DiscussionCommunityMembershipAdmin(admin.ModelAdmin):
    inlines = (DiscussionCommunityInline,)


admin.site.register(DiscussionCommunity, DiscussionCommunityAdmin)
admin.site.register(DiscussionCommunityMembership, DiscussionCommunityMembershipAdmin)

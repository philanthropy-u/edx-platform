from django.contrib import admin

from models import DiscussionCommunityMembership


class DiscussionCommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'community_url','get_course')
    raw_id_fields = ('user',)

    def get_course(self, obj):
        return obj.community_url.course_id

    get_course.short_description = 'course id'
    get_course.admin_order_field = 'community_url__course_id'


admin.site.register(DiscussionCommunityMembership, DiscussionCommunityMembershipAdmin)

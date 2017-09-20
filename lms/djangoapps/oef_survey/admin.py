"""
django admin pages for OEF survey model
"""

from oef_survey.models import (OefSurvey, CategoryPage, SubCategory, SurveyQuestion, SurveyQuestionAnswer,
                               UserSurveyFeedback, SurveyFeedback)
from ratelimitbackend import admin


@admin.register(OefSurvey)
class OefSurveyAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CategoryPage)
class CategoryPageAdmin(admin.ModelAdmin):
    fields = ('name', 'survey', 'description')
    list_display = ('name', 'survey', 'is_complete')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fields = ('survey', 'category', 'name', 'description',)
    list_display = ('name', 'survey', 'category',)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ('statement',)


@admin.register(SurveyQuestionAnswer)
class SurveyQuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'category',)


admin.site.register(SurveyFeedback)
admin.site.register(UserSurveyFeedback)

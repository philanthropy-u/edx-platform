"""
django admin pages for OEF survey model
"""

from oef_survey.models import OefSurvey, CategoryPage, SubCategory, SurveyQuestion, SurveyQuestionAnswer
from ratelimitbackend import admin


@admin.register(OefSurvey)
class OefSurveyAdmin(admin.ModelAdmin):
    """Admin for OEF Survey"""
    fields = ('name',)
    list_display = ('name',)

    def has_delete_permission(self, request, obj=None):
    	return False


@admin.register(CategoryPage)
class CategoryPageAdmin(admin.ModelAdmin):
    """Admin for OEF Survey"""
    fields = ('name', 'survey', 'description')
    list_display = ('name', 'survey', 'is_complete')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Admin for OEF Survey"""
    fields = ('survey', 'category', 'name', 'description',)
    list_display = ('name', 'survey', 'category',)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    """Admin for OEF Survey"""
    list_display = ('statement', )


@admin.register(SurveyQuestionAnswer)
class SurveyQuestionAnswerAdmin(admin.ModelAdmin):
    """Admin for OEF Survey"""
    list_display = ('question', 'category', )
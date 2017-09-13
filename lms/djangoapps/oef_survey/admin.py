"""
django admin pages for OEF survey model
"""

from oef_survey.models import OefSurvey, CategoryPage, SubCategory, SurveyQuestion, SurveyQuestionAnswer
from ratelimitbackend import admin


admin.site.register(OefSurvey)
admin.site.register(CategoryPage)
admin.site.register(SubCategory)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyQuestionAnswer)
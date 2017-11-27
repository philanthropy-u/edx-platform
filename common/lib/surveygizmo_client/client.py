from surveygizmo import SurveyGizmo
from django.conf import settings


class SurveyGizmoClient(SurveyGizmo):
    def __init__(self):
        """Instantiates the SurveyGizmo API Client.
        """

        return super(SurveyGizmoClient, self).__init__(
            api_version='v4',
            api_token=settings.SURVEY_GIZMO_API_TOKEN,
            api_token_secret=settings.SURVEY_GIZMO_API_TOKEN_SECRET,
        )

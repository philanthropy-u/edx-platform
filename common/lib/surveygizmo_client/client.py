from django.conf import settings
from surveygizmo import SurveyGizmo


class SurveyGizmoClient(SurveyGizmo):
    def __init__(self):
        """Instantiates the SurveyGizmo API Client.
        """

        return super(SurveyGizmoClient, self).__init__(
            api_version='v4',
            api_token=settings.SURVEY_GIZMO_TOKEN,
            api_token_secret=settings.SURVEY_GIZMO_TOKEN_SECRET,
        )

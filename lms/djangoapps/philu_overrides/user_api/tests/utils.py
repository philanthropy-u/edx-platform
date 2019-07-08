from common.djangoapps.third_party_auth.tests.utils import ThirdPartyOAuthTestMixinFacebook

class ThirdPartyOAuthTestMixinGoogle(object):
    """Tests oauth with the Google backend"""
    BACKEND = "google-oauth2"
    USER_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    # In google-oauth2 responses, the "email" field is used as the user's identifier
    UID_FIELD = "email"

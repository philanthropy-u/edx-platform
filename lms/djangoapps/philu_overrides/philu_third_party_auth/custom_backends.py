from social.backends.facebook import FacebookOAuth2


class CustomFacebookOAuth(FacebookOAuth2):
    REDIRECT_STATE = False

import json

from urllib import quote_plus
from social.backends.facebook import FacebookOAuth2
from social.backends.google import GoogleOAuth2
from social.backends.linkedin import LinkedinOAuth2

from social.exceptions import AuthFailed, AuthCanceled, AuthUnknownError, \
                              AuthMissingParameter, AuthStateMissing, \
                              AuthStateForbidden, AuthTokenError
from common.djangoapps.util.philu_utils import extract_utm_params


OAUTH_STATE_PARAM_SEPARATOR = '|||||'


def _add_utm_params_to_state(state, utm_params):
    if not utm_params:
        return state

    return state + quote_plus(OAUTH_STATE_PARAM_SEPARATOR + json.dumps(utm_params))


class CustomFacebookOAuth(FacebookOAuth2):
    REDIRECT_STATE = False

    def get_or_create_state(self):
        state = super(CustomFacebookOAuth, self).get_or_create_state()
        return _add_utm_params_to_state(state, extract_utm_params(self.data))

    def validate_state(self):
        """Validate state value. Raises exception on error, returns state
        value if valid."""
        if not self.STATE_PARAMETER and not self.REDIRECT_STATE:
            return None
        state = self.get_session_state()
        request_state = self.get_request_state()

        request_state = request_state.split(OAUTH_STATE_PARAM_SEPARATOR)[0]

        if not request_state:
            raise AuthMissingParameter(self, 'state')
        elif not state:
            raise AuthStateMissing(self, 'state')
        elif not request_state == state:
            raise AuthStateForbidden(self)
        else:
            return state


class CustomLinkedinOAuth(LinkedinOAuth2):
    def get_or_create_state(self):
        state = super(CustomLinkedinOAuth, self).get_or_create_state()
        return _add_utm_params_to_state(state, extract_utm_params(self.data))

    def validate_state(self):
        """Validate state value. Raises exception on error, returns state
        value if valid."""
        if not self.STATE_PARAMETER and not self.REDIRECT_STATE:
            return None
        state = self.get_session_state()
        request_state = self.get_request_state()

        request_state = request_state.split(OAUTH_STATE_PARAM_SEPARATOR)[0]

        if not request_state:
            raise AuthMissingParameter(self, 'state')
        elif not state:
            raise AuthStateMissing(self, 'state')
        elif not request_state == state:
            raise AuthStateForbidden(self)
        else:
            return state


class CustomGoogleOAuth(GoogleOAuth2):

    def get_or_create_state(self):
        state = super(CustomGoogleOAuth, self).get_or_create_state()
        return _add_utm_params_to_state(state, extract_utm_params(self.data))

    def validate_state(self):
        """Validate state value. Raises exception on error, returns state
        value if valid."""
        if not self.STATE_PARAMETER and not self.REDIRECT_STATE:
            return None
        state = self.get_session_state()
        request_state = self.get_request_state()

        request_state = request_state.split(OAUTH_STATE_PARAM_SEPARATOR)[0]

        if not request_state:
            raise AuthMissingParameter(self, 'state')
        elif not state:
            raise AuthStateMissing(self, 'state')
        elif not request_state == state:
            raise AuthStateForbidden(self)
        else:
            return state

    def get_user_id(self, details, response):
        """Use google email as unique id"""
        if self.setting('USE_UNIQUE_USER_ID', False):
            if 'sub' in response:
                return response['sub']
            else:
                return response['id']
        else:
            return details['email']

    def get_user_details(self, response):
        """Return user details from Google API account"""
        if 'email' in response:
            email = response['email']
        else:
            email = ''

        name, given_name, family_name = (
            response.get('name', ''),
            response.get('given_name', ''),
            response.get('family_name', ''),
        )

        fullname, first_name, last_name = self.get_user_names(
            name, given_name, family_name
        )
        return {'username': email.split('@', 1)[0],
                'email': email,
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        return self.get_json(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            params={
                'access_token': access_token,
                'alt': 'json'
            }
        )

import json

from w3lib.url import add_or_replace_parameter
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from social.pipeline import partial
from logging import getLogger

from third_party_auth.pipeline import (
    AUTH_DISPATCH_URLS, AUTH_ENTRY_REGISTER_V2, AUTH_ENTRY_LOGIN, AUTH_ENTRY_REGISTER,
    AUTH_ENTRY_LOGIN_API, AUTH_ENTRY_REGISTER_API, AUTH_ENTRY_ACCOUNT_SETTINGS, AUTH_ENTRY_CUSTOM,
    AuthEntryError, redirect_to_custom_form, provider
)

from .custom_backends import OAUTH_STATE_PARAM_SEPARATOR

logger = getLogger(__name__)


@partial.partial
def ensure_user_information(strategy, auth_entry, backend=None, user=None, social=None,
                            allow_inactive_user=False, *args, **kwargs):
    """
    Ensure that we have the necessary information about a user (either an
    existing account or registration data) to proceed with the pipeline.
    """

    # We're deliberately verbose here to make it clear what the intended
    # dispatch behavior is for the various pipeline entry points, given the
    # current state of the pipeline. Keep in mind the pipeline is re-entrant
    # and values will change on repeated invocations (for example, the first
    # time through the login flow the user will be None so we dispatch to the
    # login form; the second time it will have a value so we continue to the
    # next pipeline step directly).
    #
    # It is important that we always execute the entire pipeline. Even if
    # behavior appears correct without executing a step, it means important
    # invariants have been violated and future misbehavior is likely.
    def dispatch_to_login():
        """Redirects to the login page."""
        return redirect(AUTH_DISPATCH_URLS[AUTH_ENTRY_LOGIN])

    def dispatch_to_register(auth_entry_register=AUTH_ENTRY_REGISTER, params=dict()):
        """Redirects to the registration page."""
        url = AUTH_DISPATCH_URLS[auth_entry_register]

        for k, v in params.items():
            url = add_or_replace_parameter(url, k, v)

        return redirect(url)

    def should_force_account_creation():
        """ For some third party providers, we auto-create user accounts """
        current_provider = provider.Registry.get_from_pipeline({'backend': backend.name, 'kwargs': kwargs})
        return current_provider and current_provider.skip_email_verification

    if not user:
        if auth_entry in [AUTH_ENTRY_LOGIN_API, AUTH_ENTRY_REGISTER_API]:
            return HttpResponseBadRequest()
        elif auth_entry == AUTH_ENTRY_LOGIN:
            # User has authenticated with the third party provider but we don't know which edX
            # account corresponds to them yet, if any.
            if should_force_account_creation():
                return dispatch_to_register()
            return dispatch_to_login()
        elif auth_entry == AUTH_ENTRY_REGISTER or auth_entry == AUTH_ENTRY_REGISTER_V2:
            # User has authenticated with the third party provider and now wants to finish
            # creating their edX account.
            state = strategy.request.GET.get('state', '')
            params = state.split(OAUTH_STATE_PARAM_SEPARATOR)

            if len(params) > 1:
                params = json.loads(params[-1])
                if not all([k.startswith('utm_') for k in params]):
                    params = {}
            else:
                params = {}

            return dispatch_to_register(auth_entry, params=params)
        elif auth_entry == AUTH_ENTRY_ACCOUNT_SETTINGS:
            raise AuthEntryError(backend, 'auth_entry is wrong. Settings requires a user.')
        elif auth_entry in AUTH_ENTRY_CUSTOM:
            # Pass the username, email, etc. via query params to the custom entry page:
            return redirect_to_custom_form(strategy.request, auth_entry, kwargs)
        else:
            raise AuthEntryError(backend, 'auth_entry invalid')

    if not user.is_active:
        # The user account has not been verified yet.
        if allow_inactive_user:
            # This parameter is used by the auth_exchange app, which always allows users to
            # login, whether or not their account is validated.
            pass
        elif social is None:
            # The user has just registered a new account as part of this pipeline. Their account
            # is inactive but we allow the login to continue, because if we pause again to force
            # the user to activate their account via email, the pipeline may get lost (e.g.
            # email takes too long to arrive, user opens the activation email on a different
            # device, etc.). This is consistent with first party auth and ensures that the
            # pipeline completes fully, which is critical.
            pass
        else:
            # This is an existing account, linked to a third party provider but not activated.
            # Double-check these criteria:
            assert user is not None
            assert social is not None
            # We now also allow them to login again, because if they had entered their email
            # incorrectly then there would be no way for them to recover the account, nor
            # register anew via SSO. See SOL-1324 in JIRA.
            # However, we will log a warning for this case:
            logger.warning(
                'User "%s" is using third_party_auth to login but has not yet activated their account. ',
                user.username
            )


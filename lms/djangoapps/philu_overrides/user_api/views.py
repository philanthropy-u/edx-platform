from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from openedx.core.djangoapps.user_api.helpers import shim_student_view, require_post_params

from openedx.core.djangoapps.user_api.views import LoginSessionView


class LoginSessionViewCustom(LoginSessionView):
    @method_decorator(require_post_params(["email", "password"]))
    @method_decorator(csrf_protect)
    def post(self, request):
        # For the initial implementation, shim the existing login view
        # from the student Django app.
        from philu_overrides.views import login_user_custom
        return shim_student_view(login_user_custom, check_logged_in=True)(request)


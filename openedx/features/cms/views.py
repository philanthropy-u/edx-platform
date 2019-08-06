from edxmako.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
@ensure_csrf_cookie
def automate_rerun(request):
    return render_to_response('rerun/automate_rerun.html')

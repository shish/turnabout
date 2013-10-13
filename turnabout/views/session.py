import logging

from .meta import *

log = logging.getLogger(__name__)


@view_config(request_method="POST", route_name="sessions", renderer="json")
def session_create(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    duser = User.by_name(username)
    if duser and duser.check_password(password):
        request.response.headers.extend(remember(request, duser))
        log.info("User %(username)s logged in", {"username": duser.username})
        return TTResponse(status="ok")
    else:
        return TTResponse(status="error")


@view_config(request_method="DELETE", route_name="session", renderer="json")
def session_delete(request):
    request.response.headers.extend(forget(request))
    log.info("User %(username)s logged out", {"username": request.user.username})
    return TTResponse(status="ok")

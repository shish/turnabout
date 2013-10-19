import logging
from pyramid.security import remember, forget

from .meta import *

log = logging.getLogger(__name__)


@view_config(request_method="POST", route_name="sessions", renderer="json")
def session_create(request):
    username = request.json_body.get("username", "")
    password = request.json_body.get("password", "")

    duser = User.by_username(username)
    if duser and duser.check_password(password):
        request.response.headers.extend(remember(request, duser))
        log.info("User %(username)s logged in", {"username": duser.username})
        return TTResponse(status="ok")
    else:
        if not duser:
            log.info("User %(username)s not found", {"username": request.json_body.get("username", "")})
        else:
            log.info("Password check failed for %(username)s", {"username": duser.username})
        return TTResponse(status="error")


@view_config(request_method="DELETE", route_name="session", renderer="json")
def session_delete(request):
    request.response.headers.extend(forget(request))
    log.info("User %(username)s logged out", {"username": request.user.username})
    return TTResponse(status="ok")

import logging

from .meta import *

log = logging.getLogger(__name__)


@view_config(request_method="POST", route_name="sessions", renderer="json")
def session_create(request):
    return TTResponse(status="ok")


@view_config(request_method="DELETE", route_name="session", renderer="json")
def session_delete(request):
    return TTResponse(status="ok")

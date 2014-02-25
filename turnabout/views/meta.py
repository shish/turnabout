import hashlib
import time

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.exceptions import NotFound, Forbidden
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from turnabout.models import (
    DBSession,
    Tracker,
    StoryType,
    Story,
    Attachment,
    Comment,
    User,
    )

import os


class TTResponse(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __json__(self, request):
        return self.__dict__


@view_config(route_name='index', renderer='string')
def index(request):
    fn = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    return Response(open(fn).read(), content_type="text/html")


@view_config(context=NotFound, renderer="json")
def not_found(request):
    return {"status": "error", "code": "404"}


@view_config(context=Forbidden, renderer="json")
def forbidden(request):
    return {"status": "error", "code": "403"}

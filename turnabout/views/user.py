from .meta import *


@view_config(request_method="GET", route_name="user", renderer="json")
def user_read(request):
    try:
        user_id = int(request.matchdict["user_id"])
        user = DBSession.query(User).filter(User.user_id==user_id).one()
        return user
    except (NoResultFound, ValueError):
        raise NotFound("User %r not found" % user_id)


@view_config(request_method="PUT", route_name="user", renderer="json")
def user_update(request):
    try:
        user_id = int(request.matchdict["user_id"])
        user = DBSession.query(User).filter(User.user_id==user_id).one()
        if "name" in request.json_body:
            user.name = request.json_body["name"]
        if "username" in request.json_body:
            user.username = request.json_body["username"]
        if "email" in request.json_body:
            user.email = request.json_body["email"]
        return user
    except (NoResultFound, ValueError):
        raise NotFound("User %r not found" % user_id)

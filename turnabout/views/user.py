from .meta import *


@view_config(request_method="GET", route_name="user", renderer="json")
def user_read(request):
    try:
        user_id = int(request.matchdict["user_id"])
        user = DBSession.query(User).filter(User.user_id==user_id).one()
        return user
    except (NoResultFound, ValueError):
        raise NotFound("User %r not found" % user_id)
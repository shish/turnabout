from .meta import *


@view_config(request_method="GET", route_name="storytypes", renderer="json")
def storytype_list(request):
    storytype = DBSession.query(StoryType).filter(StoryType.tracker_id==request.matchdict["tracker_id"]).all()
    return storytype
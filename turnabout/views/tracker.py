from .meta import *


@view_config(request_method="GET", route_name="trackers", renderer="json")
def tracker_list(request):
    tracker = DBSession.query(Tracker).all()
    return tracker


@view_config(request_method="POST", route_name="trackers", renderer="json")
def tracker_create(request):
    tracker = Tracker(
        name=request.json_body["name"],
        title=request.json_body["title"],
    )
    tracker.storytypes.append(StoryType(
        name=u"Feature",
        fields={
            "points": "Integer(0, 12)",
            "state": "State(['iced:scheduled','scheduled:started'])",
            "requester": "User()",
            "owner": "User()",
        }
    ))
    tracker.storytypes.append(StoryType(
        name=u"Bug",
        fields={
            "points": "Integer(0, 12)",
            "state": "State(['iced:scheduled','scheduled:started'])",
            "requester": "User()",
            "owner": "User()",
        }
    ))

    DBSession.add(tracker)
    DBSession.flush()
    return TTResponse(status="ok", tracker_id=tracker.tracker_id)


@view_config(request_method="GET", route_name="tracker", renderer="json")
def tracker_read(request):
    try:
        tracker_id = int(request.matchdict["tracker_id"])
        tracker = DBSession.query(Tracker).filter(Tracker.tracker_id==tracker_id).one()
        return tracker
    except (NoResultFound, ValueError):
        raise NotFound()


@view_config(request_method="PUT", route_name="tracker", renderer="json")
def tracker_update(request):
    try:
        tracker_id = int(request.matchdict["tracker_id"])
        tracker = DBSession.query(Tracker).filter(Tracker.tracker_id==tracker_id).one()
        tracker.name = request.json_body["name"]
        tracker.title = request.json_body["title"]
        return TTResponse(status="ok")
    except (NoResultFound, ValueError):
        raise NotFound()

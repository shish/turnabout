from .meta import *


@view_config(request_method="GET", route_name="stories", renderer="json")
def story_list(request):
    story = DBSession.query(Story).filter(Story.tracker_id==request.matchdict["tracker_id"]).order_by(Story.rank).all()
    return story


@view_config(request_method="POST", route_name="stories", renderer="json")
def story_create(request):
    storytype = DBSession.query(StoryType).filter(StoryType.tracker_id==request.matchdict["tracker_id"]).first()
    story = Story(
        tracker_id=request.matchdict["tracker_id"],
        title=request.json_body.get("title", ""),
        description=request.json_body.get("description", ""),
        storytype=storytype,
        rank=time.time(),
        draft=True,
    )
    DBSession.add(story)
    DBSession.flush()
    return TTResponse(status="ok", story_id=story.story_id)


@view_config(request_method="GET", route_name="story", renderer="json")
def story_read(request):
    try:
        tracker_id = int(request.matchdict["tracker_id"])
        story_id = int(request.matchdict["story_id"])
        story = DBSession.query(Story).filter(Story.story_id==story_id, Story.tracker_id==tracker_id).one()
        return story
    except (NoResultFound, ValueError):
        raise NotFound("Story %r not found" % story_id)


@view_config(request_method="PUT", route_name="story", renderer="json")
def story_update(request):
    try:
        story_id = int(request.matchdict["story_id"])
        story = DBSession.query(Story).filter(Story.story_id==story_id).one()

        if "title" in request.json_body:
            story.title = request.json_body["title"]
        if "description" in request.json_body:
            story.description = request.json_body["description"]
        if "rank" in request.json_body:
            story.rank = request.json_body["rank"]
        if "state_id" in request.json_body:
            story.state_id = request.json_body["state_id"]

        story.draft = False
        fields = {}
        fields.update(story.fields)
        fields.update(request.json_body["fields"])
        for n in fields.keys():
            if fields[n] is None or fields[n] == "":
                del fields[n]
        story.fields = fields
        return TTResponse(status="ok")
    except (NoResultFound, ValueError):
        raise NotFound("Story %r not found" % request.matchdict.get("story_id"))


@view_config(request_method="DELETE", route_name="story", renderer="json")
def story_delete(request):
    try:
        tracker_id = int(request.matchdict["tracker_id"])
        story_id = int(request.matchdict["story_id"])
        story = DBSession.query(Story).filter(Story.story_id==story_id, Story.tracker_id==tracker_id).one()
        DBSession.delete(story)
        return TTResponse(status="ok")
    except (NoResultFound, ValueError):
        raise NotFound("Story %r not found" % request.matchdict.get("story_id"))


from pyramid.response import Response
from pyramid.view import view_config
from pyramid.exceptions import NotFound, Forbidden

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from .models import (
    DBSession,
    Tracker,
    StoryType,
    Story,
    Comment,
    )


class TTResponse(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __json__(self, request):
        return self.__dict__


@view_config(route_name='index', renderer='index.mako')
def index(request):
    return {}


@view_config(context=NotFound, renderer="json")
def not_found(request):
    return {"status": "error", "code": "404"}


@view_config(context=Forbidden, renderer="json")
def forbidden(request):
    return {"status": "error", "code": "403"}


#######################################################################
# Tracker

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


#######################################################################
# Story Types

@view_config(request_method="GET", route_name="storytypes", renderer="json")
def storytype_list(request):
    storytype = DBSession.query(StoryType).filter(StoryType.tracker_id==request.matchdict["tracker_id"]).all()
    return storytype


#######################################################################
# Story

@view_config(request_method="GET", route_name="stories", renderer="json")
def story_list(request):
    story = DBSession.query(Story).filter(Story.tracker_id==request.matchdict["tracker_id"]).all()
    return story


@view_config(request_method="POST", route_name="stories", renderer="json")
def story_create(request):
    storytype = DBSession.query(StoryType).filter(StoryType.tracker_id==request.matchdict["tracker_id"], StoryType.name==request.json_body["type"]).one()
    story = Story(
        tracker_id=request.matchdict["tracker_id"],
        title=request.json_body["title"],
        description=request.json_body["description"],
        storytype=storytype,
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
        story.title = request.json_body["title"]
        story.description = request.json_body["description"]
        fields = {}
        fields.update(story.fields)
        fields.update(request.json_body["fields"])
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


#######################################################################
# Comment

@view_config(request_method="POST", route_name="comments", renderer="json")
def comment_create(request):
    comment = Comment(
        story_id=request.matchdict["story_id"],
        user_id=request.user.user_id,
        text=request.json_body["text"]
    )
    DBSession.add(comment)
    DBSession.flush()
    return TTResponse(status="ok", comment_id=comment.comment_id)


@view_config(request_method="DELETE", route_name="comment", renderer="json")
def comment_delete(request):
    try:
        comment_id = int(request.matchdict["comment_id"])
        comment = DBSession.query(Comment).filter(Comment.comment_id==comment_id).one()
        DBSession.delete(comment)
        return TTResponse(status="ok")
    except (NoResultFound, ValueError):
        raise NotFound()

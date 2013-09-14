from pyramid.response import Response
from pyramid.view import view_config

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


#######################################################################
# Tracker

@view_config(request_method="GET", route_name="trackers", renderer="json")
def tracker_list(request):
    tracker = DBSession.query(Tracker).all()
    return tracker


@view_config(request_method="GET", route_name="tracker", renderer="json")
def tracker_read(request):
    try:
        tracker_id = int(request.matchdict["tracker_id"])
        tracker = DBSession.query(Tracker).filter(Tracker.id==tracker_id).one()
        return tracker
    except NoResultFound:
        return TTResponse(status="error", message="Tracker %r not found" % tracker_id)


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
    type = DBSession.query(StoryType).filter(StoryType.tracker_id==request.matchdict["tracker_id"], StoryType.name==request.json_body["type"]).one()
    story = Story(
        tracker_id=request.matchdict["tracker_id"],
        title=request.json_body["title"],
        description=request.json_body["description"],
        type=type,
    )
    DBSession.add(story)
    DBSession.flush()
    return TTResponse(status="ok", story_id=story.id)


@view_config(request_method="GET", route_name="story", renderer="json")
def story_read(request):
    try:
        story = DBSession.query(Story).filter(Story.id==request.matchdict["story_id"]).one()
        return story
    except NoResultFound:
        return TTResponse(status="error")


@view_config(request_method="PUT", route_name="story", renderer="json")
def story_update(request):
    story = DBSession.query(Story).filter(Story.id==request.matchdict["story_id"]).one()
    story.title = request.json_body["title"]
    story.description = request.json_body["description"]
    fields = {}
    fields.update(story.fields)
    fields.update(request.json_body["fields"])
    story.fields = fields
    return TTResponse(status="ok")


@view_config(request_method="DELETE", route_name="story", renderer="json")
def story_delete(request):
    story = DBSession.query(Story).filter(Story.id==request.matchdict["story_id"]).one()
    DBSession.delete(story)
    return TTResponse(status="ok")


#######################################################################
# Comment

@view_config(request_method="POST", route_name="comments", renderer="json")
def comment_create(request):
    comment = Comment(
        story_id=request.matchdict["story_id"],
        user_id=request.user.id,
        text=request.json_body["text"]
    )
    DBSession.add(comment)
    DBSession.flush()
    return TTResponse(status="ok", comment_id=comment.id)


@view_config(request_method="DELETE", route_name="comment", renderer="json")
def comment_delete(request):
    comment = DBSession.query(Comment).filter(Comment.id==request.matchdict["comment_id"]).one()
    DBSession.delete(comment)
    return TTResponse(status="ok")

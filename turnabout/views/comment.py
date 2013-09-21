from .meta import *


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

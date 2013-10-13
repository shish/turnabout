from .meta import *
import logging

log = logging.getLogger(__name__)


@view_config(request_method="POST", route_name="comments", renderer="json")
def comment_create(request):
    story_id = int(request.matchdict["story_id"])
    comment = Comment(
        story_id=story_id,
        user_id=request.user.user_id,
        text=request.json_body["text"]
    )
    DBSession.add(comment)
    DBSession.flush()
    log.info("Added comment %(comment_id)d to story %(story_id)d", {"story_id": story_id, "comment_id": comment.comment_id})
    return TTResponse(status="ok", comment_id=comment.comment_id)


@view_config(request_method="DELETE", route_name="comment", renderer="json")
def comment_delete(request):
    try:
        comment_id = int(request.matchdict["comment_id"])
        comment = DBSession.query(Comment).filter(Comment.comment_id==comment_id).one()
        DBSession.delete(comment)
        log.info("Deleted comment %(comment_id)d", {"comment_id": comment.comment_id})
        return TTResponse(status="ok")
    except (NoResultFound, ValueError):
        raise NotFound()

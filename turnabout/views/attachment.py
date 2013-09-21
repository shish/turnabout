from .meta import *


@view_config(request_method="POST", route_name="attachments", renderer="json")
def attachment_create(request):
    data = request.POST["file"].file.read()
    attachment = Attachment(
        story_id=request.matchdict["story_id"],
        user_id=request.user.user_id,
        filename=request.POST["file"].filename,
        data=data,
        hash=hashlib.sha256(data).hexdigest(),
        mime=request.POST["file"].type,
        size=len(data),
    )
    DBSession.add(attachment)
    DBSession.flush()
    if True:  # if not xhr
        return HTTPFound("/#/tracker/"+request.matchdict["tracker_id"]+"/story/"+request.matchdict["story_id"])
    return TTResponse(status="ok", attachment_id=attachment.attachment_id)


@view_config(request_method="DELETE", route_name="attachment", renderer="json")
def attachment_delete(request):
    try:
        attachment_id = int(request.matchdict["attachment_id"])
        attachment = DBSession.query(Attachment).filter(Attachment.attachment_id==attachment_id).one()
        DBSession.delete(attachment)
        if True:  # if not xhr
            return HTTPFound("/#/tracker/"+request.matchdict["tracker_id"]+"/story/"+request.matchdict["story_id"])
        return TTResponse(status="ok")
    except (NoResultFound, ValueError) as e:
        raise NotFound(str(e))
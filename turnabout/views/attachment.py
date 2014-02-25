import logging

from six import StringIO
from .meta import *

log = logging.getLogger(__name__)


@view_config(request_method="POST", route_name="attachments", renderer="json")
def attachment_create(request):
    data = request.POST["file"].file.read()
    thumbnail = None

    if request.POST["file"].type.startswith("image/"):
        log.info("Created thumbnail for image attachment")
        try:
            from PIL import Image
            im = Image.open(StringIO(data))
            im.thumbnail((128, 128), Image.ANTIALIAS)

            thumbnailio = StringIO()
            im.save(thumbnailio, "JPEG")
            thumbnail = thumbnailio.getvalue()
        except Exception as e:
            log.info("Failed to create thumbnail: %s", e)

    attachment = Attachment(
        story_id=request.matchdict["story_id"],
        user_id=request.user.user_id,
        filename=request.POST["file"].filename,
        data=data,
        thumbnail=thumbnail,
        hash=hashlib.sha256(data).hexdigest(),
        mime=request.POST["file"].type,
        size=len(data),
    )
    DBSession.add(attachment)
    DBSession.flush()
    if True:  # if not xhr
        return HTTPFound("/#/tracker/"+request.matchdict["tracker_id"]+"/story/"+request.matchdict["story_id"])
    return TTResponse(status="ok", attachment_id=attachment.attachment_id)


@view_config(request_method="GET", route_name="attachment", renderer="string")
def attachment_read(request):
    try:
        attachment_id = int(request.matchdict["attachment_id"])
        attachment = DBSession.query(Attachment).filter(Attachment.attachment_id==attachment_id).one()
        if request.GET.get("format") == "thumbnail":
            request.response.content_type = "image/jpeg"
            if attachment.thumbnail:
                log.info("Showing attachment thumb")
                return attachment.thumbnail
            else:
                log.info("Showing generic thumb")
                return file(os.path.join(os.path.dirname(__file__), "..", "static/img/thumbnail.png")).read()
        else:
            log.info("Showing full attachment")
            request.response.content_type = str(attachment.mime)
            return attachment.data
    except (NoResultFound, ValueError) as e:
        raise NotFound(str(e))


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

from .meta import *
from .story import Story
from .user import User


class Attachment(Base):
    __tablename__ = "attachment"
    attachment_id = Column(Integer, primary_key=True)
    filename = Column(Unicode, nullable=False)
    data = Column(LargeBinary, nullable=False)
    hash = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    mime = Column(String, nullable=False)
    story_id = Column(Integer, ForeignKey("story.story_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    posted = Column(DateTime, nullable=False, default=func.now())

    story = relationship(Story, backref=backref("attachments", cascade="all, delete-orphan"))
    user = relationship(User, backref=backref("attachments", cascade="all, delete-orphan"))

    def __json__(self, request):
        d = {
            "attachment_id": self.attachment_id,
            "filename": self.filename,
            "hash": self.hash,
            "data_url": "x",
            "thumbnail_url": "/static/img/thumbnail.png",
            "posted": str(self.posted)[:16],
        }
        if "tracker_id" in request.matchdict:
            d["tracker_id"] = request.matchdict["tracker_id"]
        if "story_id" in request.matchdict:
            d["story_id"] = request.matchdict["story_id"]
        return d
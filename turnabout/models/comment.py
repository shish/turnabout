from .meta import *
from .story import Story
from .user import User


class Comment(Base):
    __tablename__ = "comment"
    comment_id = Column(Integer, primary_key=True)
    story_id = Column(Integer, ForeignKey("story.story_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    text = Column(Unicode, nullable=False)
    posted = Column(DateTime, nullable=False, default=func.now())

    story = relationship(Story, backref=backref("comments", cascade="all, delete-orphan"))
    user = relationship(User, backref=backref("comments", cascade="all, delete-orphan"))

    def __json__(self, request):
        d = {
            "comment_id": self.comment_id,
            "user": self.user,
            "text": self.text,
            "posted": str(self.posted)[:16],
        }
        if "tracker_id" in request.matchdict:
            d["tracker_id"] = request.matchdict["tracker_id"]
        if "story_id" in request.matchdict:
            d["story_id"] = request.matchdict["story_id"]
        return d

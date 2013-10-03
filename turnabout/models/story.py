from .meta import *
from .storytype import StoryType, State
from .tracker import Tracker


class Story(Base):
    __tablename__ = "story"
    story_id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    tracker_id = Column(Integer, ForeignKey("tracker.tracker_id"), nullable=False)
    state_id = Column(Integer, ForeignKey("state.state_id"), nullable=False)
    type_id = Column(Integer, ForeignKey("storytype.storytype_id"), nullable=False)
    description = Column(Unicode, nullable=False, default=u"")
    rank = Column(Float, nullable=False)  # default = time.time()
    fields = Column(JSONEncodedDict, nullable=False, default={})
    draft = Column(Boolean, nullable=False, default=False)

    storytype = relationship(StoryType)
    state = relationship(State)
    tracker = relationship(Tracker, backref=backref("stories", cascade="all, delete-orphan"))

    def __json__(self, request):
        d = {
            "tracker_id": self.tracker_id,
            "story_id": self.story_id,
            "title": self.title,
            "storytype_id": self.type_id,
            "state_id": self.state_id,
            "fields": self.fields,
            "rank": self.rank,
        }
        if "story_id" in request.matchdict:
            d.update({
                #"storytype": self.storytype,
                "description": self.description,
                "comments": self.comments,
                "attachments": self.attachments,
            })
        return d
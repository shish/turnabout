from .meta import *
from .tracker import Tracker


class StoryType(Base):
    __tablename__ = "storytype"
    storytype_id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer, ForeignKey("tracker.tracker_id"), nullable=False)
    name = Column(Unicode, nullable=False)
    fields = Column(postgresql.HSTORE, nullable=False, default={})

    tracker = relationship(Tracker, backref=backref("storytypes", cascade="all, delete-orphan"))

    def __json__(self, request):
        return {
            "storytype_id": self.storytype_id,
            "name": self.name,
            "fields": self.fields,
        }
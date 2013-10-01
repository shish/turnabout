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
            "states": dict([(st.state_id, st) for st in self.states]),
        }


class State(Base):
    __tablename__ = "state"
    state_id = Column(Integer, primary_key=True)
    storytype_id = Column(Integer, ForeignKey("storytype.storytype_id"), nullable=False)
    name = Column(Unicode, nullable=False)
    color = Column(String, nullable=False)

    storytype = relationship(StoryType, backref=backref("states", cascade="all, delete-orphan"))

    def __json__(self, request):
        return {
            #"state_id": self.state_id,
            "storytype_id": self.storytype_id,
            "name": self.name,
            "color": self.color,
            "next_links": self.next_links,
        }


class Transition(Base):
    __tablename__ = "transition"
    old_state_id = Column(Integer, ForeignKey("state.state_id"), primary_key=True)
    state_id = Column(Integer, ForeignKey("state.state_id"), primary_key=True)
    label = Column(Unicode, nullable=False)

    old_state = relationship(State, foreign_keys=old_state_id, backref=backref("next_links", cascade="all, delete-orphan"))
    state = relationship(State, foreign_keys=state_id, backref=backref("prev_links", cascade="all, delete-orphan"))

    def __init__(self, f, t, l):
        self.old_state = f
        self.state = t
        self.label = l

    def __json__(self, request):
        return {
            #"old_state_id": self.old_state_id,
            "state_id": self.state_id,
            "label": self.label,
        }

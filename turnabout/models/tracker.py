from .meta import *


class Tracker(Base):
    __tablename__ = "tracker"
    tracker_id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    title = Column(Unicode(64), nullable=False)

    def __json__(self, request):
        d = {
            "tracker_id": self.tracker_id,
            "name": self.name,
            "title": self.title,
        }
        if "tracker_id" in request.matchdict:
            d.update({
                "storytypes": dict([(st.storytype_id, st) for st in self.storytypes]),
                "users": {
                    "shish": {},
                    "bob": {},
                    "fred": {},
                }
            })
        return d

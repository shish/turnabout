from sqlalchemy import (
    Column, ForeignKey, Index,
    Integer, Float,
    Text, String, Unicode,
    DateTime,
    LargeBinary,
    func,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    username = Column(Unicode(64), nullable=False)
    password = Column(String(128), nullable=False)

    @staticmethod
    def by_username(username):
        if username:
            return DBSession.query(User).filter(User.username == username).first()

    def __json__(self, request):
        d = {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
        }
        return d


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
                "storytypes": self.storytypes,
            })
        return d


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


class Story(Base):
    __tablename__ = "story"
    story_id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    tracker_id = Column(Integer, ForeignKey("tracker.tracker_id"), nullable=False)
    type_id = Column(Integer, ForeignKey("storytype.storytype_id"), nullable=False)
    description = Column(Unicode, nullable=False, default=u"")
    rank = Column(Float, nullable=False, default=1000)
    fields = Column(postgresql.HSTORE, nullable=False, default={})

    storytype = relationship(StoryType)
    tracker = relationship(Tracker, backref=backref("stories", cascade="all, delete-orphan"))

    def __json__(self, request):
        d = {
            "tracker_id": self.tracker_id,
            "story_id": self.story_id,
            "title": self.title,
            "storytype_id": self.type_id,
            "fields": self.fields,
            "rank": self.rank,
        }
        if "story_id" in request.matchdict:
            d.update({
                "storytype": self.storytype,
                "description": self.description,
                "comments": self.comments,
                "attachments": self.attachments,
            })
        return d


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


#Index('my_index', MyModel.name, unique=True, mysql_length=255)

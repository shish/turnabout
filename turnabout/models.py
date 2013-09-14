from sqlalchemy import (
    Column, ForeignKey, Index,
    Integer, Float,
    Text, String, Unicode,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    username = Column(Unicode(64), nullable=False)
    password = Column(String(128), nullable=False)

    @staticmethod
    def by_username(username):
        if username:
            return DBSession.query(User).filter(User.username == username).first()

    def __json__(self, request):
        d = {
            "id": self.id,
            "name": self.name,
            "username": self.username,
        }
        return d


class Tracker(Base):
    __tablename__ = "tracker"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    title = Column(Unicode(64), nullable=False)

    def __json__(self, request):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "types": self.storytypes,
        }


class StoryType(Base):
    __tablename__ = "storytype"
    id = Column(Integer, primary_key=True)
    tracker_id = Column(Integer, ForeignKey("tracker.id"), nullable=False)
    name = Column(Unicode, nullable=False)
    fields = Column(postgresql.HSTORE, nullable=False, default={})

    tracker = relationship(Tracker, backref="storytypes")

    def __json__(self, request):
        return {
            "id": self.id,
            "name": self.name,
            "fields": self.fields,
        }


class Story(Base):
    __tablename__ = "story"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode, nullable=False)
    tracker_id = Column(Integer, ForeignKey("tracker.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("storytype.id"), nullable=False)
    description = Column(Unicode, nullable=False, default=u"")
    rank = Column(Float, nullable=False, default=1000)
    fields = Column(postgresql.HSTORE, nullable=False, default={})

    type = relationship(StoryType)
    tracker = relationship(Tracker, backref="stories")

    def __json__(self, request):
        d = {
            "id": self.id,
            "title": self.title,
            "type": self.type.name,
            "fields": self.fields,
            "rank": self.rank,
        }
        if "story_id" in request.matchdict:
            d.update({
                "description": self.description,
                "comments": self.comments,
            })
        return d


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, ForeignKey("story.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    text = Column(Unicode, nullable=False)

    story = relationship(Story, backref="comments")
    user = relationship(User)

    def __json__(self, request):
        return {
            "id": self.id,
            "user": self.user,
            "text": self.text,
        }


#Index('my_index', MyModel.name, unique=True, mysql_length=255)

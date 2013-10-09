from .meta import *

import hashlib


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    email = Column(Unicode(255), nullable=False)
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
            "gravatar": hashlib.md5(self.email.strip().lower()).hexdigest().lower(),
            "username": self.username,
            "email": self.email,
        }
        return d

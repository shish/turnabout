from .meta import *

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

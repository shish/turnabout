import unittest
import transaction

from pyramid import testing

from turnabout.models import DBSession, Base, User
from turnabout.scripts.initializedb import add_stub_data


class TurnaboutTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        #Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        #DBSession.begin_nested()
        add_stub_data()

        self.user = User.by_username("shish")

    def tearDown(self):
        #DBSession.rollback()
        DBSession.remove()
        testing.tearDown()

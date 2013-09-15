import unittest
import transaction

from pyramid import testing

from turnabout.models import DBSession, Base, User
from turnabout.scripts.initializedb import add_stub_data


class TurnaboutTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

        #import paste
        #settings = paste.deploy.appconfig('config:/home/shish/Projects/turnabout/development.ini')

        from sqlalchemy import create_engine
        engine = create_engine('postgres://shish:shish@localhost/test')
        DBSession.configure(bind=engine)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        add_stub_data()

        self.user = User.by_username("shish")

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

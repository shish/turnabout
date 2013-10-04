from pyramid import testing
from pyramid.exceptions import NotFound

from turnabout.tests import TurnaboutTest
from turnabout.views import user_read


class TestUserRead(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"user_id": "1"})
        user = user_read(request)
        self.assertEqual(user.username, "shish")

    def test_fail(self):
        request = testing.DummyRequest(matchdict={"user_id": "9999"})
        self.assertRaises(NotFound, user_read, request)

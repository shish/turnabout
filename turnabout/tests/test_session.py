from pyramid import testing
from pyramid.exceptions import NotFound

from turnabout.tests import TurnaboutTest
from turnabout.views import session_create, session_delete


class TestSessionCreate(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(json_body={"username": u"test", "password": u"test"})
        resp = session_create(request)
        self.assertEqual(resp.status, "ok")

    def test_fail(self):
        request = testing.DummyRequest(json_body={"username": u"test", "password": u"arrr"})
        resp = session_create(request)
        self.assertEqual(resp.status, "ok")


class TestSessionDelete(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest()
        resp = session_delete(request)
        self.assertEqual(resp.status, "ok")

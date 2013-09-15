from pyramid import testing
from pyramid.exceptions import NotFound

from turnabout.tests import TurnaboutTest
from turnabout.views import tracker_list, tracker_create, tracker_read, tracker_update


class TestTrackerList(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest()
        trackers = tracker_list(request)
        self.assertEqual(trackers[0].name, 'tt')


class TestTrackerCreate(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(user=self.user, json_body={
            "name": "mytracker",
            "title": u"A new tracker",
        })
        resp = tracker_create(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": resp.tracker_id})
        trackers = tracker_list(request)
        self.assertEqual(trackers[-1].title, u"A new tracker")


class TestTrackerRead(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"})
        tracker = tracker_read(request)
        self.assertEqual(tracker.name, 'tt')

    def test_fail(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "9999"})
        self.assertRaises(NotFound, tracker_read, request)

        request = testing.DummyRequest(matchdict={"tracker_id": "moo"})
        self.assertRaises(NotFound, tracker_read, request)


class TestTrackerUpdate(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"}, json_body={"name": "renamed", "title": "New Title"})
        resp = tracker_update(request)
        self.assertEqual(resp.status, 'ok')

        request = testing.DummyRequest(matchdict={"tracker_id": "1"})
        tracker = tracker_read(request)
        self.assertEqual(tracker.name, 'renamed')

    def test_fail(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "9999"}, json_body={"name": "renamed", "title": "New Title"})
        self.assertRaises(NotFound, tracker_read, request)

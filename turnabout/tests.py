import unittest
import transaction

from pyramid import testing
from pyramid.exceptions import NotFound

from .models import DBSession, Base, User
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


from .views import index

class TestIndex(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest()
        info = index(request)
        self.assertEqual(info, {})


from .views import tracker_list, tracker_create, tracker_read, tracker_update

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


from .views import storytype_list

class TestStoryTypeList(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"})
        storytypes = storytype_list(request)
        self.assertEqual(storytypes[0].name, 'feature')


from .views import story_list, story_create, story_read, story_update, story_delete

class TestStoryList(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"})
        stories = story_list(request)
        self.assertEqual(stories[0].title, 'A Feature Story')
        self.assertNotIn('Another Bug Story (in another tracker)', [s.title for s in stories])


class TestStoryCreate(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"}, user=self.user, json_body={
            "title": u"A new story",
            "description": u"",
            "type": u"feature",
        })
        resp = story_create(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": resp.story_id})
        story = story_read(request)
        self.assertEqual(story.title, u"A new story")


class TestStoryRead(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.title, "A Feature Story")

    def test_fail(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "9999"})
        self.assertRaises(NotFound, story_read, request)

        request = testing.DummyRequest(matchdict={"tracker_id": "9999", "story_id": "1"})
        self.assertRaises(NotFound, story_read, request)


class TestStoryUpdate(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"}, user=self.user, json_body={
            "title": u"A new story (updated)",
            "description": u"now with description",
            "type": u"feature",
            "fields": {
                "points": u"5",
            }
        })
        resp = story_update(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.title, "A new story (updated)")
        self.assertEqual(story.fields["points"], u"5")


class TestStoryDelete(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"}, user=self.user, json_body={
            "title": u"A new story",
            "description": u"",
            "type": u"feature",
        })
        resp = story_create(request)
        self.assertEqual(resp.status, "ok")
        self.assertIsNotNone(resp.story_id)

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": resp.story_id})
        resp2 = story_delete(request)
        self.assertEqual(resp2.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": resp.story_id})
        self.assertRaises(NotFound, story_read, request)

    def test_fail(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "9999"})
        self.assertRaises(NotFound, story_delete, request)

        request = testing.DummyRequest(matchdict={"tracker_id": "9999", "story_id": "1"})
        self.assertRaises(NotFound, story_delete, request)


from .views import comment_create, comment_delete

class TestCommentCreate(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"}, json_body={"text": u"test comment"}, user=self.user)
        resp = comment_create(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.comments[-1].text, u"test comment")

class TestCommentDelete(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"}, json_body={"text": u"test comment"}, user=self.user)
        resp = comment_create(request)
        self.assertEqual(resp.status, "ok")
        self.assertIsNotNone(resp.comment_id)

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1", "comment_id": resp.comment_id})
        resp = comment_delete(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertNotEqual(story.comments[-1].text, u"test comment")

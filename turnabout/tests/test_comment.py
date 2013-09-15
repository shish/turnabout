from pyramid import testing
from pyramid.exceptions import NotFound

from turnabout.tests import TurnaboutTest
from turnabout.views import comment_create, comment_delete
from turnabout.views import story_read


class TestCommentCreate(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"}, json_body={"text": u"test comment"}, user=self.user)
        resp = comment_create(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.comments[-1].text, u"test comment")


class TestCommentDelete(TurnaboutTest):
    def test_pass(self):
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

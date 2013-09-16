from pyramid import testing
from pyramid.exceptions import NotFound

from turnabout.tests import TurnaboutTest
from turnabout.views import story_list, story_create, story_read, story_update, story_delete


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
            "storytype": u"feature",
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
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.title, "A Feature Story")
        self.assertEqual(story.fields["points"], u"3")
        self.assertEqual(story.fields["requester"], u"shish")
        self.assertNotIn("reward", story.fields)

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"}, user=self.user, json_body={
            "title": u"A new story (updated)",
            "description": u"now with description",
            "storytype": u"feature",
            "fields": {
                "points": u"5",     # update
                "requester": None,  # delete
                "reward": "cake",   # create
            }
        })
        resp = story_update(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.title, "A new story (updated)")
        self.assertEqual(story.fields["points"], u"5")
        self.assertEqual(story.fields["reward"], u"cake")
        self.assertNotIn("requester", story.fields)


class TestStoryDelete(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"}, user=self.user, json_body={
            "title": u"A new story",
            "description": u"",
            "storytype": u"feature",
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

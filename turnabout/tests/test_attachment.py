from pyramid import testing
from pyramid.exceptions import NotFound
from mock import Mock
from StringIO import StringIO

from turnabout.tests import TurnaboutTest
from turnabout.views import attachment_create, attachment_read, attachment_delete
from turnabout.views import story_read


class TestAttachmentCreate(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(
            matchdict={"tracker_id": "1", "story_id": "1"},
            POST={
                "file": Mock(
                    filename=u"test.dat",
                    file=StringIO("test data"),
                    type="text/plain",
                ),
            },
            user=self.user
        )
        resp = attachment_create(request)
        self.assertEqual(resp.status, "302 Found")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.attachments[-1].filename, u"test.dat")
        self.assertEqual(story.attachments[-1].hash, "916f0027a575074ce72a331777c3478d6513f786a591bd892da1a577bf2335f9")


class TestAttachmentRead(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1", "attachment_id": "1"}, GET={"format": "data"})
        resp = attachment_read(request)
        self.assertEqual(request.response.content_type, "text/plain")
        self.assertEqual(resp, "hello world!")

    def test_pass_thumb(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1", "attachment_id": "1"}, GET={"format": "thumbnail"})
        resp = attachment_read(request)
        self.assertEqual(request.response.content_type, "image/jpeg")
        self.assertEqual(resp, "thumb")


class TestAttachmentDelete(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1", "attachment_id": "1"})
        resp = attachment_delete(request)
        self.assertEqual(resp.status, "302 Found")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(len(story.attachments), 0)

from pyramid import testing
from pyramid.exceptions import NotFound
from mock import Mock
from six import StringIO
import six

from turnabout.tests import TurnaboutTest
from turnabout.views import attachment_create, attachment_read, attachment_delete
from turnabout.views import story_read

png1x1 = (
    '\x89PNG\r\n\x1a\n'
    '\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00:~\x9bU'
    '\x00\x00\x00\nIDAT\x08\xd7c\xf8\x0f\x00\x01\x01\x01\x00\x1b\xb6\xeeV'
    '\x00\x00\x00\x00IEND\xaeB`\x82\n'
)


class TestAttachmentCreate(TurnaboutTest):
    def test_pass_plain(self):
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

    def test_pass_image(self):
        request = testing.DummyRequest(
            matchdict={"tracker_id": "1", "story_id": "1"},
            POST={
                "file": Mock(
                    filename=u"1x1.png",
                    file=StringIO(png1x1),
                    type="image/png",
                ),
            },
            user=self.user
        )
        resp = attachment_create(request)
        self.assertEqual(resp.status, "302 Found")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(story.attachments[-1].filename, u"1x1.png")
        self.assertEqual(story.attachments[-1].hash, "119dfc24dc533791fb48a646096b3f191fef420c934e25dcb61d036a5554e211")


class TestAttachmentRead(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1", "attachment_id": "1"}, GET={"format": "data"})
        resp = attachment_read(request)
        self.assertEqual(request.response.content_type, "text/plain")
        self.assertEqual(resp, six.binary_type("hello world!", "utf8"))

    def test_pass_thumb(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1", "attachment_id": "1"}, GET={"format": "thumbnail"})
        resp = attachment_read(request)
        self.assertEqual(request.response.content_type, "image/jpeg")
        self.assertEqual(resp, six.binary_type("thumb", "utf8"))


class TestAttachmentDelete(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1", "attachment_id": "1"})
        resp = attachment_delete(request)
        self.assertEqual(resp.status, "302 Found")

        request = testing.DummyRequest(matchdict={"tracker_id": "1", "story_id": "1"})
        story = story_read(request)
        self.assertEqual(len(story.attachments), 0)

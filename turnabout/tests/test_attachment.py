from pyramid import testing
from pyramid.exceptions import NotFound
from mock import Mock
from StringIO import StringIO

from turnabout.tests import TurnaboutTest
from turnabout.views import attachment_create
from turnabout.views import story_read


class TestAttachmentCreate(TurnaboutTest):
    def test_pass(self):
        request = testing.DummyRequest(
            matchdict={"tracker_id": "1", "story_id": "1"},
            POST={
                "file": Mock(
                    filename=u"test.dat",
                    file=StringIO("test data"),
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

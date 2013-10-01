from pyramid import testing

from turnabout.tests import TurnaboutTest
from turnabout.views import index


class TestIndex(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest()
        info = index(request)
        #self.assertEqual(info, {})

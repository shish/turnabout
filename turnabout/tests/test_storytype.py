from pyramid import testing

from turnabout.tests import TurnaboutTest
from turnabout.views import storytype_list


class TestStoryTypeList(TurnaboutTest):
    def test(self):
        request = testing.DummyRequest(matchdict={"tracker_id": "1"})
        storytypes = storytype_list(request)
        self.assertEqual(storytypes[0].name, 'Feature')

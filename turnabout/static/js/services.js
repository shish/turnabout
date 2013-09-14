
angular.module('turnaboutServices', ['ngResource'])
	.factory('Tracker', function($resource) {
		return $resource('tracker/:tracker_id', {tracker_id: "@tracker_id"}, {
			query: {method:'GET', params:{}, isArray:true}
		});
	})
	.factory('StoryType', function($resource) {
		return $resource('tracker/:tracker_id/storytype/:storytype_id', {tracker_id: "@tracker_id", storytype_id: "@storytype_id"});
	})
	.factory('Story', function($resource) {
		return $resource('tracker/:tracker_id/story/:story_id', {tracker_id: "@tracker_id", story_id: "@story_id"}, {
			save: {method:"PUT"}
		});
	})
	.factory('Comment', function($resource) {
		return $resource('tracker/:tracker_id/story/:story_id/comment/:comment_id', {tracker_id: "@tracker_id", story_id: "@story_id", comment_id: "@comment_id"});
	})
	;

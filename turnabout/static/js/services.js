var CRUD = {
	list: {method:'GET', isArray:true},
	create: {method:"POST"},
	read: {method:'GET'},
	update: {method:"PUT"},
	delete: {method:"DELETE"},
};

angular.module('turnaboutServices', ['ngResource'])
	.factory('Tracker', function($resource) {
		return $resource('tracker/:tracker_id', {tracker_id: "@tracker_id"}, CRUD);
	})
	.factory('StoryType', function($resource) {
		return $resource('tracker/:tracker_id/storytype/:storytype_id', {tracker_id: "@tracker_id", storytype_id: "@storytype_id"}, CRUD);
	})
	.factory('Story', function($resource) {
		return $resource('tracker/:tracker_id/story/:story_id', {tracker_id: "@tracker_id", story_id: "@story_id"}, CRUD);
	})
	.factory('Comment', function($resource) {
		return $resource('tracker/:tracker_id/story/:story_id/comment/:comment_id', {tracker_id: "@tracker_id", story_id: "@story_id", comment_id: "@comment_id"}, CRUD);
	})
	.factory('Attachment', function($resource) {
		return $resource('tracker/:tracker_id/story/:story_id/attachment/:attachment_id', {tracker_id: "@tracker_id", story_id: "@story_id", attachment_id: "@attachment_id"}, CRUD);
	})
	;

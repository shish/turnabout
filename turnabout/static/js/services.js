var CRUD = {
	list: {method:'GET', isArray:true},
	create: {method:"POST"},
	read: {method:'GET'},
	update: {method:"PUT"},
	delete: {method:"DELETE"},
};

turnabout.factory('Tracker', function($resource) {
	return $resource('tracker/:tracker_id', {tracker_id: "@tracker_id"}, CRUD);
});

turnabout.factory('StoryType', function($resource) {
	return $resource('tracker/:tracker_id/storytype/:storytype_id', {tracker_id: "@tracker_id", storytype_id: "@storytype_id"}, CRUD);
});

turnabout.factory('Story', function($resource) {
	return $resource('tracker/:tracker_id/story/:story_id', {tracker_id: "@tracker_id", story_id: "@story_id"}, CRUD);
});

turnabout.factory('Comment', function($resource) {
	return $resource('tracker/:tracker_id/story/:story_id/comment/:comment_id', {tracker_id: "@tracker_id", story_id: "@story_id", comment_id: "@comment_id"}, CRUD);
});

turnabout.factory('Attachment', function($resource) {
	return $resource('tracker/:tracker_id/story/:story_id/attachment/:attachment_id', {tracker_id: "@tracker_id", story_id: "@story_id", attachment_id: "@attachment_id"}, CRUD);
});

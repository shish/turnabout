
function getStoryType(tracker, name) {
	for(t in tracker.storytypes) {
		if(t.name == name) return t;
	}
}

function HeaderCtrl($scope, $routeParams, Tracker) {
	if(!$scope.tracker) {
		if($routeParams.tracker_id) {
			$scope.tracker = Tracker.read({tracker_id: $routeParams.tracker_id});
		}
		else {
			$scope.tracker = null;
		}
	}

	if(!$scope.trackers) {
		$scope.trackers = Tracker.list();
	}
}

function TrackerListCtrl($scope, Tracker) {
	$scope.trackers = Tracker.list();
}

function TrackerCreateCtrl($scope, $route, $routeParams, Tracker) {
	var blank_tracker = {
		name: "",
		title: "",
	};

	$scope.tracker = angular.copy(blank_tracker);
	$scope.save = function() {
		Tracker.create($scope.tracker, function(response) {
			$scope.tracker.tracker_id = response.tracker_id;
			$scope.trackers.push($scope.tracker);
			$scope.tracker = angular.copy(blank_tracker);
		});
	};
}

function TrackerReadCtrl($scope, $routeParams, Tracker, Story, StoryType) {
	$scope.tracker = Tracker.read({tracker_id: $routeParams.tracker_id});
	$scope.stories = Story.query({tracker_id: $routeParams.tracker_id});
	$scope.storytypes = StoryType.query({tracker_id: $routeParams.tracker_id});

	$scope.save = function() {
		Tracker.update(angular.copy($scope.tracker), function() {
			//alert("Saved");
		});
	};
}

function StoryCreateCtrl($scope, $route, $routeParams, $location, Story) {
	$scope.story = {
		tracker_id: $routeParams.tracker_id,
	};

	$scope.create = function() {
		Story.create($scope.story, function(response) {
			$scope.story.story_id = response.story_id;
			$location.path("/tracker/"+$scope.story.tracker_id+"/story/"+$scope.story.story_id);
		});
	};
}

function StoryReadCtrl($scope, $route, $routeParams, $location, Tracker, Story, Comment, Attachment) {
	$scope.tracker = Tracker.read({tracker_id: $routeParams.tracker_id});
	$scope.story = Story.get({tracker_id: $routeParams.tracker_id, story_id: $routeParams.story_id});

	$scope.edit = function() {
		$scope.story_pre_edit = angular.copy($scope.story);
		$scope.story.editing = true;
	};
	$scope.save = function() {
		Story.update(angular.copy($scope.story), function() {
			$scope.story.editing = false;
		});
	};
	$scope.cancel = function() {
		$scope.story = angular.copy($scope.story_pre_edit);
	};
	$scope.delete = function() {
		Story.remove($scope.story, function() {
			$location.path("/tracker/"+$routeParams.tracker_id);
		});
	};
	$scope.comment_delete = function(comment) {
		Comment.remove(comment, function() {
			var index = $scope.story.comments.indexOf(comment);
			$scope.story.comments.splice(index, 1);
		});
	};
	$scope.attachment_delete = function(attachment) {
		Attachment.remove(attachment, function() {
			var index = $scope.story.attachments.indexOf(attachment);
			$scope.story.attachments.splice(index, 1);
		});
	};
}

function CommentCreateCtrl($scope, $route, $routeParams, Comment) {
	var blank_comment = {
		user: {
			name: 'shish',
		},
		tracker_id: $routeParams.tracker_id,
		story_id: $routeParams.story_id,
		text: "",
	};

	$scope.comment = angular.copy(blank_comment);
	$scope.save = function() {
		Comment.create($scope.comment, function(response) {
			$scope.comment.comment_id = response.comment_id;
			$scope.story.comments.push($scope.comment);
			$scope.comment = angular.copy(blank_comment);
		});
	};
}

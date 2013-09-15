
function getStoryType(tracker, name) {
	for(t in tracker.storytypes) {
		if(t.name == name) return t;
	}
}

function HeaderCtrl($scope, $routeParams, Tracker) {
	if($routeParams.tracker_id) {
		$scope.tracker = Tracker.get({tracker_id: $routeParams.tracker_id});
	}
	else {
		$scope.tracker = {
			title: "Turnabout Tracker",
		};
	}
}

function TrackerListCtrl($scope, Tracker) {
	$scope.trackers = Tracker.query();
}

function TrackerCreateCtrl($scope, $route, $routeParams, Tracker) {
	var blank_tracker = {
		name: "",
		title: "",
	};

	$scope.tracker = angular.copy(blank_tracker);
	$scope.save = function() {
		Tracker.save($scope.tracker, function() {
			$scope.trackers.push($scope.tracker);
			$scope.tracker = angular.copy(blank_tracker);
		});
	};
}

function TrackerReadCtrl($scope, $routeParams, Tracker, Story, StoryType) {
	$scope.tracker = Tracker.get({tracker_id: $routeParams.tracker_id});
	$scope.stories = Story.query({tracker_id: $routeParams.tracker_id});
	$scope.storytypes = StoryType.query({tracker_id: $routeParams.tracker_id});

	$scope.save = function() {
		Tracker.save(angular.copy($scope.tracker), function() {
			alert("Saved");
		});
	};
}

function StoryCreateCtrl($scope, $route, $routeParams, Story) {
	$scope.story = {
		tracker_id: $routeParams.tracker_id,
	};
}

function StoryReadCtrl($scope, $route, $routeParams, Tracker, Story, Comment) {
	$scope.tracker = Tracker.get({tracker_id: $routeParams.tracker_id});
	$scope.story = Story.get({tracker_id: $routeParams.tracker_id, story_id: $routeParams.story_id});

	$scope.edit = function() {
		$scope.story.editing = true;
	};
	$scope.save = function() {
		Story.save(angular.copy($scope.story), function() {
			$scope.story.editing = false;
			alert("Saved");
		});
	};
	$scope.delete = function() {
		Story.remove($scope.story, function() {
			$route.location("/tracker/"+$routeParams.tracker_id);
		});
	};
	$scope.comment_delete = function(comment) {
		Comment.remove(comment, function() {
			// delete story.comments[X];  // only deletes part of the HTML?
			$route.reload();
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
		Comment.save($scope.comment, function() {
			$scope.story.comments.push($scope.comment);
			$scope.comment = angular.copy(blank_comment);
		});
	};
}

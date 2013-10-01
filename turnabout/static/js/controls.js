
function getStoryType(tracker, storytype_id) {
	console.log("Getting storytype", storytype_id);
	for(t in tracker.storytypes) {
		if(t.storytype_id == storytype_id) return t;
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
	$scope.sortableOptions = {
		stop: function(e, ui) {
			var ss = $scope.stories;
			var prev, current, next;

			for(var i=0; i<ss.length; i++) {
				current = ss[i];

				if(i == 0) prev = {rank: 0};
				else prev = ss[i-1];

				if(i == ss.length-1) next = {rank: 9999};
				else next = ss[i+1];

				// each story should be ranked higher than the one before
				// (highest rank is 0)
				if(current.rank > prev.rank) {
					// we cool
				}
				else {
					// this element is out of order. Make it the average
					// of the element before and after (assumes that only
					// one element will ever be out of order at a time)
					current.rank = prev.rank + 0.1; // (prev.rank + next.rank) / 2;
					console.log("Re-ranking "+current.title+" as "+current.rank);
					Story.update(angular.copy(ss[i]));
				}
			}
		}
	};

	$scope.setState = function(story, state_id) {
		story.state_id = state_id;
		Story.update(angular.copy(story));
	}

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
	$scope.story = Story.get({tracker_id: $routeParams.tracker_id, story_id: $routeParams.story_id}, function() {
		if(!$scope.story.title) {
			$scope.story.editing = true;
		}
	});

	$scope.edit = function() {
		$scope.story_pre_edit = angular.copy($scope.story);
		$scope.story.editing = true;
	};
	$scope.save = function() {
		if($scope.story.story_id) {
			Story.update(angular.copy($scope.story), function() {
				$scope.story.editing = false;
			});
		}
		else {
			Story.create(angular.copy($scope.story), function(result) {
				$location.path("/tracker/"+$routeParams.tracker_id+"/story/"+result.story_id);
				$scope.story.editing = false;
			});
		}
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

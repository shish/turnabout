<!--
vim:ft=html
-->
<html ng-app="turnabout">
	<head>
		<title>Turnabout Tracker</title>
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
		<script src="//code.angularjs.org/1.2.0-rc.2/angular.js"></script>
		<script src="//code.angularjs.org/1.2.0-rc.2/angular-route.js"></script>
		<script src="//code.angularjs.org/1.2.0-rc.2/angular-resource.js"></script>
		<script>

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
		return $resource('tracker/:tracker_id/story/:story_id', {tracker_id: "@tracker_id", story_id: "@story_id"});
	})
	.factory('Comment', function($resource) {
		return $resource('tracker/:tracker_id/story/:story_id/comment/:comment_id', {tracker_id: "@tracker_id", story_id: "@story_id", comment_id: "@comment_id"});
	})
	;

angular.module('turnabout', ['ngRoute', 'turnaboutServices'])
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider.
			when('/tracker', {templateUrl: 'static/partials/tracker-list.html', controller: TrackerListCtrl}).
			when('/tracker/:tracker_id', {templateUrl: 'static/partials/tracker-read.html', controller: TrackerReadCtrl}).
			when('/tracker/:tracker_id/story/:story_id', {templateUrl: 'static/partials/story-read.html', controller: StoryReadCtrl}).
			otherwise({redirectTo: '/tracker'});
	}])
	;

function TrackerListCtrl($scope, Tracker) {
	$scope.trackers = Tracker.query();
}

function TrackerReadCtrl($scope, $routeParams, Tracker, Story, StoryType) {
	$scope.tracker = Tracker.get({tracker_id: $routeParams.tracker_id});
	$scope.stories = Story.query({tracker_id: $routeParams.tracker_id});
	$scope.storytypes = StoryType.query({tracker_id: $routeParams.tracker_id});
}

function StoryCreateCtrl($scope, $route, $routeParams, Story) {
	$scope.story = {
		tracker_id: $routeParams.tracker_id,
	};
}

function StoryReadCtrl($scope, $route, $routeParams, Tracker, Story, Comment) {
	$scope.tracker = Tracker.get({tracker_id: $routeParams.tracker_id});
	$scope.story = Story.get({tracker_id: $routeParams.tracker_id, story_id: $routeParams.story_id});

	$scope.comment_delete = function(comment_id) {
		var comment = Comment.remove({tracker_id: $routeParams.tracker_id, story_id: $routeParams.story_id, "comment_id": comment_id}, function() {
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
		</script>
	</head>
	<body>
		<div ng-view></div>
	</body>
</html>


angular.module('turnabout', ['ngRoute', 'turnaboutServices', 'ui.sortable'])
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider.
			when('/tracker', {templateUrl: 'static/partials/tracker-list.html', controller: TrackerListCtrl}).
			when('/tracker/:tracker_id', {templateUrl: 'static/partials/tracker-read.html', controller: TrackerReadCtrl}).
			when('/tracker/:tracker_id/story/:story_id', {templateUrl: 'static/partials/story-read.html', controller: StoryReadCtrl}).
			otherwise({redirectTo: '/tracker'});
	}])
	;

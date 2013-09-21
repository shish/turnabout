
angular.module('turnabout', ['ngRoute', 'turnaboutServices', 'ui.sortable', 'angular.markdown'])
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider.
			when('/tracker', {templateUrl: 'static/partials/tracker-list.html', controller: TrackerListCtrl}).
			when('/tracker/:tracker_id', {templateUrl: 'static/partials/tracker-read.html', controller: TrackerReadCtrl}).
			when('/tracker/:tracker_id/story/:story_id', {templateUrl: 'static/partials/story-read.html', controller: StoryReadCtrl}).
			otherwise({redirectTo: '/tracker'});
	}])
	.filter('groupCount', function() {
		return function(input, count) {
			if(!input) return [];
			var rows = [];
			for (var i = 0; i < input.length; i++) {
				if ( i % count == 0) rows.push([]);
				rows[rows.length-1].push(input[i]);
			}
			return rows;
		}
	})
	;

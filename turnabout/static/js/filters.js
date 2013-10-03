turnabout.filter('groupCount', function() {
	return function(input, count) {
		if(!input) return [];
		var rows = [];
		for (var i = 0; i < input.length; i++) {
			if ( i % count == 0) rows.push([]);
			rows[rows.length-1].push(input[i]);
		}
		return rows;
	}
});

turnabout.filter('stateToClass', function() {
	return function(input) {
		return "state-" + input.replace(/[^a-zA-Z]/g, '');
	}
});

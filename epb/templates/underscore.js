(function() {
	window._ = {
		each: function (collection, callback) {
			for (var i = 0; i < collection.length; ++i) {
				callback(collection[i]);
			};
		},
		reduce: function (collection, callback, total) {
			_.each(collection, function (element) {
				total = callback(total, element);
			});
			return total;
		},
		map: function (collection, callback) {
			return _.reduce(collection, function (total, element) {
				total.push(callback(element));
				return total;
			}, []);
		},
		sum: function (collection, callback) {
			return _.reduce(collection, function(total, element) {
				total = total + callback(element);
				return total;
			}, 0);
		}
	}
})();
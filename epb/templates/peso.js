(function() {

	var $ = window.$ = function(selector, parent) {
		if (!parent) { parent = document };
		return parent.querySelector(selector);
	}
	$.size = function(element) {
		var style = window.getComputedStyle(element, null);
		var width = parseInt(style.getPropertyValue("width"));
		var height = parseInt(style.getPropertyValue("height"));
		return {width: width, height: height};
	}

	var Template = window.Template = function(id) {
		this.template = document.getElementById(id);
	}
	Template.prototype = {
		apply: function (element) {
			element.innerHTML = this.template.innerHTML;
		},
		asElement: function () {
			var holder = document.createElement("div");
			holder.innerHTML = this.template.innerHTML;
			return holder.children[0];
		}
	}

	var View = window.View = (function(){
		var _init = function(opts) {
			if (!opts) { opts = {}; }
			this.model = opts.model;
			this.element = opts.element;
		}
		var _$ = function(selector) {
			return $(selector, this.element);
		}
		var extend = function(prototype) {
			var klass = function() {
				_init.apply(this, arguments);
				if (this.init) { this.init.apply(this, arguments); };
				if (this.render) { this.render(); };
			};
			klass.prototype = prototype;
			klass.prototype.$ = _$;
			return klass;
		}
		return { extend: extend };
	})();
	
})();
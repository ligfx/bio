Raphael.fn.epb = {
	drawDomains: function(domains, callback) {
		var self = this;
		_.each(domains, function (domain) {
			var s = parseInt(domain.query_start * self.width);
			var w = parseInt(domain.query_width * self.width);
			
			var rect = self.rect(s, 0, w, self.height);
			rect.node.removeAttribute("fill");
			rect.node.removeAttribute("stroke");
			
			if (callback) { callback(self, rect, domain); };
		});
	},
	drawMidline: function(attr) {
		var mid = parseInt(this.height / 2) + 0.5;
		this.path("M0 " + mid + "L" + this.width + " " + mid);
	},
	resizeToParent: function() {
		var size = $.size(this.canvas.parentNode);
		this.setSize(size.width, size.height);
	}
}

var RulerView = View.extend({
	init: function() {
		this.endCap = this.$("#rulerLegendEnd");
	},
	render: function() {
		this.endCap.innerHTML = this.model.width;
	},
});

var ProteinDomainsHeaderView = View.extend({
	init: function() {
		this.paper = Raphael(this.element);
	},
	render: function() {
		this.paper.epb.resizeToParent();
		this.paper.epb.drawMidline();
		this.paper.epb.drawDomains(this.model, function(paper, rect, domain) {
			var text = paper.text(rect.getBBox().x, paper.height / 2, domain.name);
			text.attr({"text-anchor": "start"});
			text.node.removeAttribute("style");
			text.node.removeAttribute("stroke");
			text.node.removeAttribute("fill");
			
			rect.attr({"href": domain.url});
			text.insertAfter(rect);
		})
	}
});

var ProteinDomainsBackgroundView = View.extend({
	init: function() {
		this.paper = Raphael(this.element);
	},
	render: function() {
		this.paper.epb.resizeToParent();
		this.paper.epb.drawDomains(this.model)
	}
});

var HSPRenderer = function(hsp) {
	this.hsp = hsp;
}
HSPRenderer.prototype = {
	height: function() { return 5; },
	drawOn: function(paper) {
		var x = parseInt(this.hsp.query_start * paper.width);
		var y = 0;
		var h = this.height();
		var w = parseInt(this.hsp.query_width * paper.width);
		return paper.rect(x, y, w, h);
	}
}

var AlignmentCanvas = View.extend({
	init: function(opts) {
		this.paper = Raphael(opts.parent, 1, 1);
		this.element = this.paper.canvas;
		this.element.removeAttribute("style");
	},
	render: function() {
		var renderers = _.map(this.model.hsps, function (hsp) {
			return new HSPRenderer(hsp);
		})
		
		this.paper.clear();
		this.paper.setSize(1, 1);
		var height = _.sum(renderers, function(r) { return r.height(); })
		var width = $.size(this.element.parentNode).width;
		this.paper.setSize(width, height);	
		
		var y_offset = 0;
		var self = this;
		_.each(renderers, function(hsp) {
			hsp.drawOn(self.paper).translate(0, y_offset);
			y_offset = y_offset + hsp.height();
		})
	}
})

var AlignmentView = View.extend({
	init: function(opts) {
		this.element = new Template("alignmentTemplate").asElement();
		opts.parent.appendChild(this.element);
		
		this.checkbox = this.$(".alignmentSelection input");
		this.link = this.$(".alignmentGraphic > a");
		this.canvas = new AlignmentCanvas({
			parent: this.link,
			model: this.model,
		});
	},
	render: function() {
		this.checkbox.value = this.model.uid;
		this.link.href = this.model.url;
	}
})

var OrganismView = View.extend({
	init: function(opts) {
		this.element = new Template("organismTemplate").asElement();
		opts.parent.appendChild(this.element);
		
		this.name = this.$(".organismName a");
		this.link = this.name;
		this.phylogeny = this.$(".organismPhylogeny");
		this.graphic = this.$(".organismGraphic");
		
		var self = this;
		_.each(this.model.alignments, function(alignment) {
			var view = new AlignmentView({
				parent: self.graphic,
				model: alignment
			});
		});
	},
	render: function() {
		this.name.innerHTML = this.model.name;
		this.link.href = this.model.url;
		this.phylogeny.innerHTML = this.model.phylogeny;
	}
})

var OrganismListView = View.extend({
	init: function() {
		var self = this;
		_.each(self.model, function(organism) {
			new OrganismView({
				parent: self.element,
				model: organism,
			});
		});
	},
})

var AppView = View.extend({
	init: function() {
		new RulerView({
			model: { width: Data.input_width },
			element: this.$("#ruler")
		})
		new ProteinDomainsHeaderView({
			model: Data.domains,
			element: this.$("#proteinDomainsHeader")
		})
		new OrganismListView({
			model: Data.organisms,
			element: this.$("#organisms")
		})
		new ProteinDomainsBackgroundView({
			model: Data.domains,
			element: this.$("#proteinDomainsBackground")
		})
	},
})
var App = new AppView({ element: document.body });
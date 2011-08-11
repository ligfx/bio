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
	init: function() {
		this.paper = Raphael();
		this.element = this.paper.canvas;
		this.element.removeAttribute("style");
	},
	render: function() {
		var renderers = _.map(this.model.hsps, function (hsp) {
			return new HSPRenderer(hsp);
		})
		
		var height = _.sum(renderers, function(r) { return r.height(); })
		var width = $.size(this.element).width;
		this.paper.setSize(width, height);
		this.paper.clear();
		
		var y_offset = 0;
		var self = this;
		_.each(renderers, function(hsp) {
			hsp.drawOn(self.paper).translate(0, y_offset);
			y_offset = y_offset + hsp.height();
		})
	}
})

var AlignmentView = View.extend({
	init: function() {
		this.element = new Template("alignmentTemplate").asElement();
		this.checkbox = this.$(".alignmentSelection input");
		this.link = this.$(".alignmentGraphic > a");
		this.canvas = new AlignmentCanvas({ model: this.model })
		this.link.appendChild(this.canvas.element);
	},
	render: function() {
		this.checkbox.value = this.model.uid;
		this.link.href = this.model.url;
	}
})

var OrganismView = View.extend({
	init: function() {
		this.element = new Template("organismTemplate").asElement();
		this.name = this.$(".organismName a");
		this.link = this.name;
		this.phylogeny = this.$(".organismPhylogeny");
		
		var self = this;
		_.each(this.model.alignments, function(alignment) {
			var view = new AlignmentView({ model: alignment });
			self.$(".organismGraphic").appendChild(view.element);
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
			var view = new OrganismView({
				model: organism,
			});
			self.element.appendChild(view.element);
		});
	}
})

var Data = {
	input_width: {{ input_width }},
	domains: [
		{% for domain in domains %}
		{
			query_start: {{ domain.query_start / input_width }},
			query_width: {{ domain.query_width / input_width }},
			name: "{{ domain.name }}",
			url: "{{ domain.url }}",
		},
		{% endfor %}
	],
	organisms: [
		{% for organism, data in data.by_organism() %}
		{
			name: "{{organism.name}}",
			phylogeny: "{{organism.info.detail_group}}",
			url: "{{organism.info.url}}",
			alignments: [
				{% for alignment, data in data.by_alignment() %}
				{
					uid: "{{ organism.slug }}:{{ alignment.name }}",
					url: "alignments/{{ alignment.digest }}.html",
					hsps: [
						{% for hsp, datum in data.by_hsp() %}
							{
								query_start: {{ hsp.query_start / input_width }},
								query_width: {{ hsp.query_width / input_width }}
							},
						{% endfor %}
					]
				},
				{% endfor %}
			]
		},
		{% endfor %}
	]
}

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
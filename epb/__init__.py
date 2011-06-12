from collections import namedtuple
import jinja2
from os import path

from epb.blast import *
from epb.fasta import *
from epb.taxon import *
from epb.utils import *

EPB_MODULEDIR = path.dirname(__file__)
	
class Figure:
	def __init__(self):
		self.header = []
		self.header.append('<?xml version="1.0" standalone="no"?>')
		self.header.append('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
		
		self.colors = {
			"Plantae": "green",
			"Opisthokonta": "orchid",
			"Amoebozoa": "purple",
			"Excavate": "yellow",
			"Chromalveolate": "orange",
			"Rhizaria": "blue"
		}
		
		self.body = []
	
	def xml(self, *args):
		self.body.append(xmlfoo.xml(*args))
	
	def draw_legend(self, **kwargs):
		height = kwargs['height']
		size = kwargs['size']
		y = kwargs['y']
		yt = y + size + (height - size) / 4
		
		for organism in self.colors.keys():
			self.xml("text", {
				"x": 15,
				"y": yt,
				"font-family": "Arial",
				"font-size": size,
				"font-weight": "bold",
				"fill": "black"},
				(organism,)
			)
			self.xml("rect", {
				"x": 10,
				"y": y,
				"width": 150,
				"height": height,
				"fill": self.colors[organism],
				"opacity": 0.2}
			)
			y += height
			yt += height
	
	def draw_scale(self):
		self.xml("text", {
			"x": 302, "y": 50,
			"font-family": "Arial", "font-size": 20,
			"font-weight": "bold", "fill": "black"
			},
			("Color key for alignment scores",)
		)
		x = 200
		y = 60
		scale = {
			"black": "&lt;40",
			"blue": "40&ndash;50",
			"lime": "50&ndash;80",
			"fuchsia": "80&ndash;200",
			"red": "&lt;=200"
		}
		for key in scale:
			self.xml("rect", {
				"x": x, "y": y,
				"width": 100, "height": 17,
				"fill": key
			})
			self.xml("text", {
				"x": x + 30, "y": y + 14,
				"font-family": "Arial", "font-size": 15, "font-weigth": "bold",
				"fill": "white"},
				(scale[key],)
			)
			x += 100
	
	def draw_sequences(self, fasta):
		length = len(Fasta.normalize(fasta))
		seqs = Fasta.each(fasta)
		
		# important parameter to shrink sequences BECAUSE i played with the CSS I have exactly 900px of width 200 is for the Organism name leaves 700 for sequence
		shrink = length/700.0;
		x=200;
		y=170;
		y_rect = y + len(seqs)*12;
		y_vert = y_rect + 20;
		switch = "white";
		for s in seqs:
			if switch == 'white':
				switch = 'blue'
			else:
				switch = 'white'
			self.xml("text", {
				"x": x, "y": y,
				"font-family": "Arial", "font-size": 10, "font-weight": "bold",
				"fill": "black"},
				(s.name,)
			)
			self.xml("line", {
				"x1": x, "x2": x,
				"y1": y, "y2": y_rect,
				"stroke": "gray"
			})
			rx = len(s.body) / shrink
			self.xml("rect", {
				"x": x, "y": y_rect,
				"width": rx, "height": 20,
				"fill": "red", "stroke": "black"
			})
			xt = x + 5
			yt = y_rect + 16
			self.xml("text", {
				"x": xt, "y": yt,
				"font-family": "Arial", "font-size": 15, "font-weight": "bold",
				"fill": "white"},
				("%i nt" % len(s.body),)
			)
			self.xml("rect", {
				"x": x, "y": y_vert,
				"width": rx, "height": "TOKEN1",
				"fill": switch, "fill-opacity": 0.2,
				"stroke": "black"
			})
			x += rx
			y += 12
		
	def __str__(self):
		svg = xmlfoo.xml("svg", {
			"width": "100%",
			"height": "100%",
			"version": "1.1",
			"xmlns": "http://www.w3.org/2000/svg",
			"xmlns:xlink": "http://www.w3.org/1999/xlink" },
			self.body
		)
		return "\n".join(self.header + [svg])

Organism = namedtuple("Organism", "name matches")

class OrganismMatch:
	def __init__(self, name, seq, hsp):
		self.name = name
		
		if hsp.score < 40:
			self.strength = "poor"
		elif hsp.score < 50:
			self.strength = "fair"
		elif hsp.score < 80:
			self.strength = "okay"
		elif hsp.score < 200:
			self.strength = "good"
		elif hsp.score >= 200:
			self.strength = "great"
		else:
			self.strength = ""
		
		self.start = "%s%%" % (hsp.query_start / len(seq) * 100)
		self.width = "%s%%" % ((hsp.query_end - hsp.query_start) / len(seq) * 100)
		
		self.evalue = hsp.expect

class OrganismName:
	def __init__(self, database, taxon, extra):
		self.database = database
		self.taxon = taxon
		self.extra = extra
	
	@classmethod
	def find_all_by_taxonomy(klass, taxon):
		fname = path.join(EPB_MODULEDIR, "Taxon_%s.txt" % taxon)
		if path.exists(fname):
			with open(fname) as f:
				return map(lambda s: path.join(self.dir, s),
				           TaxonFileParser.parse(f))
		else:
			raise TaxonFileError("couldn't find Taxon_%s.txt in module directory" % taxon)

class DatabaseCollection:
	def __init__(self, dir):
		self.dir = dir
	def find(self, name):
		return path.join(self.dir, name)

import sys
if __file__ == sys.argv[0]:
	taxon = sys.argv.pop()
	seq = Fasta.normalize(sys.stdin.read())
	
	db = DatabaseCollection("databases")
	organisms = []
	for organism_name in OrganismName.find_all_by_taxonomy(taxon):
		try:
			matches = []
			for record in Blaster.blast(db=db.find(organism_name.database), seq=seq):
				for a in record.alignments:
					for hsp in a.hsps:
						matches.append(OrganismMatch(a.title, seq, hsp))
			organisms.append(Organism(organism_name, matches))
		except BlastError as e:
			print "[Blaster] Error: %s" % e
	
	env = jinja2.Environment(loader = jinja2.PackageLoader('epb', 'templates'))
	template = env.get_template('results.html.jinja2')
	
	print template.render(organisms = organisms)
	

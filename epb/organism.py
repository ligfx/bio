from epb.blast import *
from epb.utils import *

class Organism:
	def __init__(self, name, matches):
		self.name = name
		self.matches = matches
	
	@classmethod
	def blast(klass, blaster=Blaster, **kwargs):
		name = require_kw(kwargs, "name")
		db = require_kw(kwargs, "db")
		seq = require_kw(kwargs, "seq")
		
		matches = []
		for record in blaster.blast(db=db, seq=seq):
			for a in record.alignments:
				for hsp in a.hsps:
					matches.append(OrganismMatch(a.hit_def, seq, hsp))
		return klass(name, matches)

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
		
		self.start = "%d%%" % (hsp.query_start * 100.0 / len(seq))
		self.width = "%d%%" % ((hsp.query_end - hsp.query_start) * 100.0 / len(seq))
		
		self.evalue = hsp.expect

class OrganismName:
	def __init__(self, database, taxon, extra=""):
		self.database = database
		self.taxon = taxon
		self.extra = extra
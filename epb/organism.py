from epb.blast import *
from epb.utils import *

class Organism:
	def __init__(self, name, hits):
		self.name = name
		self.hits = hits
	
	@classmethod
	def blast(klass, blaster=Blaster, **kwargs):
		name = require_kw(kwargs, "name")
		db = require_kw(kwargs, "db")
		seq = require_kw(kwargs, "seq")
		
		hits = []
		for record in blaster.blast(db=db, seq=seq):
			for align, desc in zip(record.alignments, record.descriptions):
				hits.append(OrganismHit(align, desc, seq))
		
		return Organism(name, hits)

class OrganismHit:
	def __init__(self, align, desc, seq):
		self.name = align.title
		self.evalue = desc.e
		
		self.hsps = [OrganismHSP(h, seq) for h in align.hsps]
		query_start = min(h._query_start for h in self.hsps)
		query_end = max(h._query_end for h in self.hsps)
		
		self.start = "%d%%" % (query_start * 100.0 / len(seq))
		self.width = "%d%%" % ((query_end - query_start) * 100.0 / len(seq))

class OrganismHSP:
	def __init__(self, hsp, seq):
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

		self._query_start = hsp.query_start
		self._query_end = hsp.query_end
		self.start = "%d%%" % (hsp.query_start * 100.0 / len(seq))
		self.width = "%d%%" % ((hsp.query_end - hsp.query_start) * 100.0 / len(seq))
		
		self.evalue = hsp.expect

class OrganismName:
	def __init__(self, database, taxon="", extra=""):
		self.database = database
		self.taxon = taxon
		self.extra = extra
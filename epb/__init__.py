from os import path

EPB_MODULEDIR = path.dirname(__file__)

class TaxonFileParser:
	@classmethod
	def parse(klass, stream):
		return map(lambda s: s.split("\t")[0],
		           stream.readlines())

class Database:
	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return self.name
	
	@classmethod
	def find_all_by_taxonomy(klass, taxon):
		fname = path.join(EPB_MODULEDIR, "Taxon_%s.txt" % taxon)
		if path.exists(fname):
			with open(fname) as f:
				return map(lambda s: Database(s),
				           TaxonFileParser.parse(f))
		else:
			return ()
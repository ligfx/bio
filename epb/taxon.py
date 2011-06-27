from os import path

class TaxonException(Exception): pass

class TaxonFileCollection:
	def __init__(self, dir):
		self.dir = dir
	
	def parse(self, name):
		fname = path.join(self.dir, "Taxon_%s.txt" % name)
		if not path.exists(fname):
			raise TaxonException, "Couldn't find 'Taxon_%s.txt'" % name
		with open(fname) as f:
			for line in f:
				yield line.strip().split("\t", 2)
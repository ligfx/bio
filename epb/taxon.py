from os import path

class TaxonFileParser:
	@classmethod
	def parse(klass, stream):
		for line in stream:
			yield line.strip().split("\t", 2)

class TaxonFileError(Exception):
	def __init__(self, value): self.value = value
	def __str__(self): return self.value

class TaxonFileCollection:
	def __init__(self, dir):
		self.dir = dir
	
	def find(self, name):
		expanded = path.join(self.dir, "Taxon_%s.txt" % name)
		if path.exists(expanded):
			return expanded
		else:
			raise TaxonFileError("couldn't find Taxon_%s.txt in %s" % (name, self.dir))
	
	def parse(self, name):
		with open(self.find(name)) as f:
			for t in TaxonFileParser.parse(f):
				yield t
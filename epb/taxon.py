from os import path

class TaxonFileParser:
	@classmethod
	def parse(klass, stream):
		for line in stream:
			yield line.strip().split("\t", 2)
			
class TaxonFileCollection:
	def __init__(self, dir):
		self.dir = dir
	
	def find(self, name):
		expanded = path.join(self.dir, "Taxon_%s.txt" % name)
		return expanded
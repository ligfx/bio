# [Back to docs.py](docs.html)
#
# Interface for reading organism names from the lists in the package `taxons` directory.
#
# Each taxon file should consist of lines in the format:
#
#     database(TAB)taxon(TAB)extra

from os import path

# === TaxonFileCollection ===
#
# Represents a directory `dir` containing taxon lists.
class TaxonFileCollection:
	
	# Taxon files are named `Taxon_%s.txt`, where `%s` is a unique name.
	filename_format = "Taxon_%s.txt"
	
	def __init__(self, dir):
		self.dir = dir
	
	# === TaxonFileCollection.parse ===
	#
	# **Takes:** _string_ `name` of taxon list to parse
	#
	# **Returns:** _iterator_ over names in file, where each name is split on the first two tab characters
	def parse(self, name):
		with self.open(name) as f:
			for line in f:
				yield line.strip().split("\t", 2)
	
	def open(self, name):
		fname = self.expand_name(name)
		self.check_file(fname)
		return open(fname)
	
	def expand_name(self, name):
		return path.join(self.dir, self.filename_format % name)
	
	def check_file(self, fname):
		if not path.exists(fname):
			raise TaxonException, "Couldn't find '%s'" % fname

# === TaxonException ===
class TaxonException(Exception): pass
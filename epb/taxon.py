class TaxonFileParser:
	@classmethod
	def parse(klass, stream):
		for line in stream:
			yield line.strip().split("\t", 2)
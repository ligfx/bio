import re

class Fasta:
	class Sequence:
		def __init__(self, s):
			header, body = s.split("\n", 1)
			self.name = header.replace('>', '').strip()
			self.body = re.sub(r"[\n\s*]", '', body).strip()
		def __repr__(self):
			return "Sequence('>%s')" % (self.name + "\n" + self.body)
	
	@classmethod
	def normalize(klass, seq):
		return "".join(map(lambda s: s.body, klass.each(seq)))
		
	@classmethod
	def each(klass, seq):
		seqs = []
		return map(Fasta.Sequence, filter(lambda s: s != '', seq.split("\n>")))
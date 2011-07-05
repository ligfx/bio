import re
from StringIO import StringIO
from Bio import SeqIO

class Fasta:
	class Sequence:
		def __init__(self, opts={}):
			self.name = opts['name']
			self.seq = opts['seq']
			
		@property
		def size(self):
			return len(self.seq)
	
	@classmethod
	def normalize(klass, seq):
		return "> Concatenated input\n" + "".join(s.seq for s in klass.each(seq))
		
	@classmethod
	def each(klass, seq):
		s = StringIO(seq)
		for r in SeqIO.parse(s, 'fasta'):
			yield Fasta.Sequence({
				"name": r.description.strip(),
				"seq": str(r.seq)
			})
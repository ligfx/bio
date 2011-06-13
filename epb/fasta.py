import re
from StringIO import StringIO
from Bio import SeqIO

class Fasta:
	class Sequence:
		def __init__(self, name, seq):
			self.name = name
			self.seq = seq
			
		@property
		def size(self):
			return len(self.seq)
	
	@classmethod
	def normalize(klass, seq):
		return "".join(s.seq for s in klass.each(seq))
		
	@classmethod
	def each(klass, seq):
		s = StringIO(seq)
		for r in SeqIO.parse(s, 'fasta'):
			yield Fasta.Sequence(r.description.strip(), str(r.seq))
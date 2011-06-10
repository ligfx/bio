import re
from StringIO import StringIO
from Bio import SeqIO

class Fasta:	
	@classmethod
	def normalize(klass, seq):
		return "".join(map(lambda s: str(s.seq), klass.each(seq)))
		
	@classmethod
	def each(klass, seq):
		s = StringIO(seq)
		return list(SeqIO.parse(s, 'fasta'))
# [Back to docs.py](docs.html)
#
# An interface for dealing with [FASTA](http://en.wikipedia.org/wiki/FASTA_format) files, providing a nice abstraction over BioPython's [SeqIO module](http://www.biopython.org/DIST/docs/api/Bio.SeqIO-module.html) and [SeqRecord class](http://www.biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html).

from StringIO import StringIO
from Bio import SeqIO

# === each(seq) ===
#
# **Takes:** a _string_ `seq` of FASTA sequences to parse
#
# **Returns:** an _iterator_ over each parsed sequence in `seq`, coerced to a `Sequence`
def each(seq):
	return map(Sequence.from_biopython, parse_string(seq))
	
# === normalize ===
#
# **Takes:** a _string_ `seq` of FASTA sequences to parse
#
# **Returns**: a _string_ of the concatenated parsed sequences
def normalize(seq):
	return "> Concatenated input\n" + "".join(s.seq for s in each(seq))

# === Sequence ===
#
# A shim over [`Bio.SeqRecord`](http://www.biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html).
class Sequence:
	# **name**: `SeqRecord.description`
	#
	# **seq**: `str(SeqRecord.seq)`
	def __init__(self, opts={}):
		self.name = opts['name']
		self.seq = opts['seq']

	# **\_\_len__**: `len(SeqRecord.seq)`
	def __len__(self):
		return len(self.seq)
	
	# === Sequence.from_biopython ===
	#
	# Creates a `Sequence` from a `Bio.SeqRecord`.
	@classmethod
	def from_biopython(klass, r):
		return klass({
			"name": r.description.strip(),
			"seq": str(r.seq),
		})

def parse_string(str):
	handle = StringIO(str)
	return parse(handle)

def parse(handle):
	return SeqIO.parse(handle, 'fasta')
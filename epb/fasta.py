# [Back to docs.py](docs.html)
#
# An interface for dealing with [FASTA](http://en.wikipedia.org/wiki/FASTA_format) files, providing a nice abstraction over BioPython's [SeqIO module](http://www.biopython.org/DIST/docs/api/Bio.SeqIO-module.html) and [SeqRecord class](http://www.biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html).

from StringIO import StringIO
from Bio import SeqIO

# === each(seq) ===

# **Takes:** a _string_ `seq` of FASTA sequences to parse
#
# **Returns:** an _iterator_ over each parsed sequence in `seq`, coerced to a `Sequence`
def each(seq):
	return map(Sequence.from_biopython, parse_string(seq))
	
# === normalize ===

# Normalizes a _string_ `seq` of FASTA sequences according to `method`:
#
# - `concat`: Concatenates sequences
# - `multiple`: Leaves input untouched
def normalize(seq, **opts):
	method = opts['method']
	
	if method == 'concat':
		return "> Concatenated input\n" + "".join(s.seq for s in each(seq))
	elif method == 'multiple':
		return seq
	else:
		raise Exception, "method must be one of 'concat' or 'multiple'"
	
	

# === Sequence ===

# A shim over [`Bio.SeqRecord`](http://www.biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html).
class Sequence:
	# **name**: `SeqRecord.name`
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
			"name": r.name.strip(),
			"seq": str(r.seq),
		})

def parse_string(str):
	handle = StringIO(str)
	return parse(handle)

def parse(handle):
	return SeqIO.parse(handle, 'fasta')
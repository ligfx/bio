# [Back to docs.py](docs.html)
#
# Various shims over BioPython's [Bio.Blast.Record class and its children](http://www.biopython.org/DIST/docs/api/Bio.Blast.Record-module.html).

import hashlib

# === RecordPresenter ===
#
# Shim over [`Bio.Blast.Record.Blast`](http://www.biopython.org/DIST/docs/api/Bio.Blast.Record.Blast-class.html)
class RecordPresenter:
	# **Properties:** `offset`, `query`, `width`
	def __init__(self, record, opts={}):
		self.offset = opts["offset"]
		self.width = record.query_length
		self.query = record.query

# === AlignmentPresenter ===
#
# Shim over [`Bio.Blast.Record.Alignment`](http://www.biopython.org/DIST/docs/api/Bio.Blast.Record.Alignment-class.html)
class AlignmentPresenter:
	# **Properties**: `digest`, `length`, `name`
	def __init__(self, align):
		self.name = align.title
		self.length = align.length
		self.digest = hashlib.md5(self.name).hexdigest()
	
	def __lt__(self, other):
		return self.name < other.name
	
	def __eq__(self, other):
		return self.name == other.name

# === HSPPresenter ===
#
# Shim over [`Bio.Blast.Record.HSP`](http://www.biopython.org/DIST/docs/api/Bio.Blast.Record.HSP-class.html)
class HSPPresenter:
	# **Properties:**
	def __init__(self, hsp):
		# `evalue`, `score`, `strength`
		self.evalue = hsp.expect
		self.score = hsp.score
		self.strength = _score_to_strength(hsp.score)
		
		# `query`, `subject`, `width`
		self.query = hsp.query
		self.subject = hsp.sbjct
		self.match = hsp.match
		
		# `query_start`, `query_end`, `query_width`
		self.query_start = hsp.query_start
		self.query_end = hsp.query_end
		self.query_width = hsp.query_end - hsp.query_start
		
		# `subject_start`, `subject_end`, `subject_width`
		self.subject_start = hsp.sbjct_start
		self.subject_end = hsp.sbjct_end
		self.subject_width = self.subject_end - self.subject_start
	
	def __lt__(self, other):
		return self.evalue < other.evalue
	
def _score_to_strength(score):
	if score < 40:     strength = "poor"
	elif score < 50:   strength = "fair"
	elif score < 80:   strength = "okay"
	elif score < 200:  strength = "good"
	elif score >= 200: strength = "great"
	else:              strength = ""
	return strength
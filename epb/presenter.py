# [Back to docs.py](docs.html)
#
# Various shims over BioPython's [Bio.Blast.Record class and its children](http://www.biopython.org/DIST/docs/api/Bio.Blast.Record-module.html).

import hashlib

# === NamePresenter ===
class NamePresenter:
	# **Properties:** `database`, `extra`, `id`, `taxon`
	def __init__(self, database, taxon="", extra=""):
		self.database = database
		self.taxon = taxon
		self.extra = extra
		
		self.id = _get_uid()

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
	# **Properties**: `digest`, `end`, `evalue`, `name`, `start`, `width`
	def __init__(self, align):
		# `digest`, `evalue`, `name`
		self.name = align.title
		self.digest = hashlib.md5(self.name).hexdigest()
		# This needs to be set later when we have the full list of HSPs (probably in DataSet).
		# If we have multiple records, they could each have the same alignment, so we want to
		# combine them all.
		self.evalue = None
		
		# `query_end`, `query_start`, `query_width`
		#hsps = map(HSPPresenter, align.hsps)
		#start = min(h.query_start for h in hsps)
		#end = max(h.query_end for h in hsps)
		
		#self.query_start = query_start
	 	#self.query_end = query_end
		#self.query_width = query_end - query_start
	
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
	
def _score_to_strength(score):
	if score < 40:     strength = "poor"
	elif score < 50:   strength = "fair"
	elif score < 80:   strength = "okay"
	elif score < 200:  strength = "good"
	elif score >= 200: strength = "great"
	else:              strength = ""
	return strength

def _get_uid():
	global PRESENTER_COUNT
	uid = PRESENTER_COUNT
	PRESENTER_COUNT += 1
	return uid
PRESENTER_COUNT = 0
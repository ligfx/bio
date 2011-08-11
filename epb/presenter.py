# [Back to docs.py](docs.html)
#
# Various shims over BioPython's [Bio.Blast.Record class and its children](http://www.biopython.org/DIST/docs/api/Bio.Blast.Record-module.html).

import epb.fasta
import hashlib
import os

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
		self.id = align.hit_id
		self.name = align.hit_def
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
		# `color`, `evalue`, `score`, `strength`
		self.evalue = hsp.expect
		self.score = hsp.score
		self.color = _score_to_color(hsp.score)
		
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
	
	# === lines(count) ===
	def lines(self, count=80):
		first = count - 7
		query = "Query: " + self.query[0:first]
		match = "Match: " + self.match[0:first]
		sbjct = "Sbjct: " + self.match[0:first]
		yield (query, match, sbjct)
		
		length = len(self.query)
		remaining = length - first
		for i in range(0, (remaining + count - 1) / count):
			start = first + count * i
			end = first + count * (i + 1)
			query = self.query[start:end]
			match = self.match[start:end]
			sbjct = self.subject[start:end]
			yield (query, match, sbjct)
			
	
	def __lt__(self, other):
		return self.evalue < other.evalue
	
def _score_to_color(score):
	if score < 40:     color = "black"
	elif score < 50:   color = "blue"
	elif score < 80:   color = "lime"
	elif score < 200:  color = "fuchsia"
	elif score >= 200: color = "red"
	else:              color = ""
	return color
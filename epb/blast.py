# [Back to docs.py](docs.html)

from Bio.Blast import NCBIXML
import epb.process as Process
from epb.presenter import *
from itertools import groupby
import logging
import os
from os import path
import shlex
from StringIO import StringIO
import subprocess
from subprocess import PIPE

# === DataSet ===
#
# Interface for working with &ldquo;rows&rdquo; of data.
class DataSet:
	# Each item in `data` is assumed to be an object of the form
	#
	#     {
	#       "organism": ...,
	#       "record": ...,
	#       "alignment": ...,
	#       "hsps": [...]
	#     }
	def __init__(self, data):
		self.data = data
	
	# === DataSet.by_organism ===
	#
	# **Returns:** sequence of `(organism, DataSet)` tuples
	def by_organism(self):
		return self._group('organism')
	
	# === DataSet.by_alignment ===
	#
	# **Returns:** sequence of `(alignment, DataSet)` tuples
	def by_alignment(self):		
		data = self._group('alignment')
		for a, d in data:
			# HSPs are guaranteed (?) to be sorted by e-value
			a.evalue = min(row['hsps'][0].evalue for row in d.items())
		
		data = sorted(data, key = lambda (a, d): a.evalue)
		return data
	
	# === DataSet.items ===
	#
	# **Returns:** sequence of all items in `data`
	def items(self):
		return self.data
		
	def _group(self, key):
		f = lambda _: _[key]
		return [(k, DataSet(list(v))) for (k, v) in groupby(sorted(self.data, key = f), f)]

# === Blast ===
#
# Interface to the `blastall` program.
class Blast:
	# Represents a directory containing BLAST databases.
	def __init__(self, opts):
		self.database_path = opts["database_path"]
		self.logger = logging.getLogger("epb[Blast]")
	
	# === Blast.find_all ===
	#
	# Blasts sequence `seq` against each database in `names`
	#
	# **Returns:** `DataSet` of `Presenter`s
	def find_all(self, seq, names):

		all = []

		for name in names:
			db = path.join(self.database_path, name.database)
			xml = self._get_xml(db, seq)

			for datum in self._parse_xml(xml, name):
				all.append(datum)

		return DataSet(all)
	
	def _get_xml(self, db, seq):
		return Process.run("blastall -p blastp -d %s -m7 -e 1e-5 -a 8" % db, "%s\n" % seq)
	
	def _parse_xml(self, xml, name):
		record_offset = 0
		for record in NCBIXML.parse(StringIO(xml)):
			O = name
			R = RecordPresenter(record, {"offset": record_offset})
			record_offset += R.width
			for alignment in record.alignments:
				A = AlignmentPresenter(alignment)
				H = map(HSPPresenter, alignment.hsps)
				yield {"organism": O, "record": R, "alignment": A, "hsps": H}
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

class AlignmentGroup:
	def __init__(self, alignment, data):
		self.alignment = alignment
		self.data = data
	

# === DataSet ===

# Interface for working with &ldquo;rows&rdquo; of data.
class DataSet:
	# Each item in `data` is assumed to be an object of the form
	#
	#     {
	#       "organism": ...,
	#       "record": ...,
	#       "alignment": ...,
	#       "hsp": ...
	#     }
	def __init__(self, data):
		self.data = data
	
	# === by_organism ===
	def by_organism(self):
		return self._group('organism')
	
	# === by_record ===
	def by_record(self):
		return self._group('record')

	# === by_alignment ===
	def by_alignment(self):
		data = self._group('alignment')
		data.sort(key=lambda (a, d): d.lowest_evalue())
		return data
	
	# === by_hsp ===
	
	# Unlike the other grouping functions, `by_hsp` returns a single datum, not a whole `DataSet`.
	def by_hsp(self):
		data = self._group('hsp')
		return [(hsp, next(iter(d))) for (hsp, d) in data]
	
	# === lowest_evalue ===
	def lowest_evalue(self):
		return min(d['hsp'].evalue for d in self.data)
		
	# === \_\_iter__ ===
	def __iter__(self):
		return iter(self.data)
		
	def _group(self, key):
		f = lambda _: _[key]
		scope = sorted(self.data, key = f)
		groups = groupby(scope, f)
		return [(group, DataSet(list(data))) for (group, data) in groups]

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

		import random
		random.shuffle(all)
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
				hsps = map(HSPPresenter, alignment.hsps)
				for H in hsps:
					yield {"organism": O, "record": R, "alignment": A, "hsp": H}
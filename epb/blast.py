from Bio.Blast import NCBIXML
from epb.presenter import *
from itertools import groupby
import logging
import os
from os import path
import shlex
from StringIO import StringIO
import subprocess
from subprocess import PIPE

class DataSet:
	def __init__(self, data):
		self.data = data
		
	def by_organism(self):
		return self._group('organism')
		
	def by_alignment(self):		
		data = self._group('alignment')
		for a, d in data:
			a.evalue = min(row['alignment'].evalue for row in d.items())
		
		data = sorted(data, key = lambda (a, d): a.evalue)
		return data
		
	def items(self):
		return self.data
		
	def _group(self, key):
		f = lambda _: _[key]
		return [(k, DataSet(list(v))) for (k, v) in groupby(sorted(self.data, key = f), f)]

class ProcessError(Exception): pass
class Process:
	@classmethod
	def run(klass, command, input):
		klass.which(shlex.split(command)[0])
		
		p = subprocess.Popen(
			shlex.split(command),
			stdin=PIPE, stdout=PIPE, stderr=PIPE
		)
		
		out, err = p.communicate(input)
		if p.returncode != 0:
			raise ProcessError, "Return code %i from '%s'\n%s" % (p.returncode, command, err)
		return out
	
	@classmethod
	def which(klass, command):
		which = reduce(lambda x, y: x or (os.path.exists(os.path.join(y, command))), os.environ['PATH'].split(os.pathsep), False)
		if not which: raise Exception, "can't find '%s' executable in PATH" % command

class BlastError(Exception): pass
class Blast:
	def __init__(self, opts):
		self.database_path = opts["database_path"]
		self.logger = logging.getLogger("epb[Blast]")
	
	def warn(self, s):
		self.logger.warn(s)
	
	def find_all(self, seq, names, opts={}):
		
		all = []
		
		for name in names:
			db = path.join(self.database_path, name.database)
			xml = Process.run("blastall -p blastp -d %s -m7 -e 1e-5 -a 8" % db, "%s\n" % seq)
	
			record_offset = 0
			for record in NCBIXML.parse(StringIO(xml)):
				# {"organism": ..., "record": ..., "alignment": ..., "hsps": ...}
				o = name
				r = RecordPresenter(record, {"offset": record_offset})
				record_offset += r.width
				for alignment in record.alignments:
					a = AlignmentPresenter(alignment)
					h = map(HSPPresenter, alignment.hsps)
					all.append({"organism": o, "record": r, "alignment": a, "hsps": h})
					
		return DataSet(all)
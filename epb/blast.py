from Bio.Blast import NCBIXML
from epb.presenter import *
from epb.utils import require_kw
import logging
import os
from os import path
import shlex
from StringIO import StringIO
import subprocess
from subprocess import PIPE

class BlastError(Exception):
	def __init__(self, value): self.value = value
	def __str__(self): return self.value

class Blast:
	def __init__(self, opts):
		self.database_path = opts["database_path"]
		self.logger = logging.getLogger("epb[Blast]")
	
	def warn(self, s):
		self.logger.warn(s)
	
	def find_all(self, seq, names, opts={}):
		
		all = []
		
		which = reduce(lambda x, y: x or (os.path.exists(os.path.join(y, "blastall"))), os.environ['PATH'].split(os.pathsep), False)
		if not which: raise Exception, "can't find 'blastall' executable in PATH"
		
		for name in names:
			db = path.join(self.database_path, name.database)
			p = subprocess.Popen(
				shlex.split("blastall -p blastp -d %s -m7 -e 1e-5 -a 8" % db),
				stdin=PIPE, stdout=PIPE, stderr=PIPE
			)
			
			out, err = p.communicate(seq + "\n")
			if p.returncode != 0:
				warn("return code of %i when blasting %s\n%s" % (p.returncode, db, err.strip()))
				p.kill()
				continue
			xml = StringIO(out)
			
			record_offset = 0
			for record in NCBIXML.parse(xml):
				# {"organism": ..., "record": ..., "alignment": ..., "hsps": ...}
				o = name
				r = RecordPresenter(record, {"offset": record_offset})
				record_offset += r.width
				for alignment in record.alignments:
					a = AlignmentPresenter(alignment)
					h = map(HSPPresenter, alignment.hsps)
					all.append({"organism": o, "record": r, "alignment": a, "hsps": h})
					
		return all
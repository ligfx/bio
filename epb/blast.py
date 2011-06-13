from Bio.Blast import NCBIXML
from epb.utils import require_kw
from StringIO import StringIO
import subprocess
from subprocess import PIPE

class BlastError(Exception):
	def __init__(self, value): self.value = value
	def __str__(self): return self.value

class Blaster:
	@classmethod
	def blast(klass, **kwargs):
		db = require_kw(kwargs, 'db')
		seq = require_kw(kwargs, 'seq')
		
		p = subprocess.Popen(
			("blastall -p blastp -d %s -F F -m7 -e 1e-5" % db).split(),
			stdin=PIPE, stdout=PIPE, stderr=PIPE)
		try:
			p.stdin.write(seq + "\n")
			out, err = p.communicate()
			if p.returncode != 0:
				raise BlastError, "return code of %i when blasting %s\n%s" % (p.returncode, db, err.strip())
			xml = StringIO(out)
			for record in NCBIXML.parse(xml):
				yield record
		except:
			if p.returncode == None: p.kill()
			raise
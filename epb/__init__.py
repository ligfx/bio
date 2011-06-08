from Bio.Blast import NCBIXML
from os import path
import re
from StringIO import StringIO
import subprocess
from subprocess import PIPE

EPB_MODULEDIR = path.dirname(__file__)

class BlastError(Exception):
	def __init__(self, value): self.value = value
	def __str__(self): return self.value

class Fasta:
	@classmethod
	def normalize(klass, seq):
		seqs = []
		for s in seq.split("\n>"):
			header, body = s.strip().split("\n", 1)
			body = re.sub(r"[\n\s\*]", '', body)
			seqs.append(body)
		return "".join(seqs)

class Blaster:
	@classmethod
	def blast(klass, **kwargs):
		db = kwargs['db']
		seq = kwargs['seq']
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

class TaxonFileParser:
	@classmethod
	def parse(klass, stream):
		return map(lambda s: s.split("\t")[0],
		           stream.readlines())

class TaxonFileError(Exception):
	def __init__(self, value): self.value = value
	def __str__(self): return self.value

class DatabaseCollection:
	def __init__(self, dir):
		self.dir = dir
	
	def find_all_by_taxonomy(self, taxon):
		fname = path.join(EPB_MODULEDIR, "Taxon_%s.txt" % taxon)
		if path.exists(fname):
			with open(fname) as f:
				return map(lambda s: path.join(self.dir, s),
				           TaxonFileParser.parse(f))
		else:
			raise TaxonFileError("couldn't find Taxon_%s.txt in module directory" % taxon)
			
import sys
if __file__ == sys.argv[0]:
	taxon = sys.argv.pop()
	seq = Fasta.normalize(sys.stdin.read())
	
	db = DatabaseCollection("databases")
	for organism in db.find_all_by_taxonomy(taxon):
		print organism
		try:
			for record in Blaster.blast(db=organism, seq=seq):
				for a in record.alignments:
					print a.title
					for hsp in a.hsps:
						print hsp.query_start
						print hsp.query_end
						print hsp.score
						print hsp.expect
		except BlastError as e:
			print "[Blaster] Error: %s" % e
		finally:
			print

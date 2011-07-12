# [Back to docs.py](docs.html)

from Bio.Blast import NCBIXML
import epb.process as Process
from epb.presenter import *
from StringIO import StringIO

# Interface to the `blastall` program.

def get_xml(db, seq):
	return Process.run("blastall -p blastp -d %s -m7 -e 1e-5 -a 8" % db, "%s\n" % seq)

def parse_xml(xml):
	record_offset = 0
	for record in NCBIXML.parse(StringIO(xml)):
		R = RecordPresenter(record, {"offset": record_offset})
		record_offset += R.width
		for alignment in record.alignments:
			A = AlignmentPresenter(alignment)
			hsps = map(HSPPresenter, alignment.hsps)
			for H in hsps:
				yield {"record": R, "alignment": A, "hsp": H}
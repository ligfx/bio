# [Back to docs.py](docs.html)

from Bio.Blast import NCBIXML
import epb.process as Process
from epb.presenter import *
import re
from StringIO import StringIO

# Interface to the `blastall` program.

class BadEValueException(Exception): pass

def get_xml(db, seq, opts):
	evalue = opts['evalue']
	if not re.match("^[\d\.\-e]*$", evalue):
		raise BadEValueException("Parameter 'evalue' can only contain digits and the characters '.', '-', and 'e'; got `%s'" % evalue)
	return Process.run("blastp -db %s -outfmt 5 -evalue %s -num_threads 8" % (db, evalue), "%s\n" % seq)

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
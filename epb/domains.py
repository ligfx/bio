import epb.process as Process
import re
import tempfile

class Domain:
	def __init__(self, opts):
		self.query_start = opts['query_start']
		self.query_end = opts['query_end']
		self.query_width = self.query_end - self.query_start
		
		self.name = opts['name']
		self.accession_name = opts['accession_name']
		self.url = "http://pfam.sanger.ac.uk/family/" + self.accession_name
		

class PfamScan:
	pfamdir = None
	
	@classmethod
	def get_domains(klass, seq):
		f = tempfile.NamedTemporaryFile(delete=False)
		f.write(seq.replace("> ", ">"))
		f.close()
		result = Process.run("pfam_scan.pl -fasta %s -dir %s" % (f.name, klass.pfamdir), '')
		return list(klass.parse_domains(result.split("\n")))
	
	@classmethod
	def parse_domains(klass, lines):
		for line in lines:
			if not line.startswith("#") and len(line.strip()) > 0:
				split = re.split(r"\s+", line)
				yield Domain({
					"query_start": int(split[1]),
					"query_end": int(split[2]),
					"accession_name": split[5],
					"name": split[6]
				})
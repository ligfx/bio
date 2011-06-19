class OrganismPresenter:
	def __init__(self, opts={}):
		self.name = opts.get("name")
		self.records = opts.get("records")
		
	@classmethod
	def from_name_and_records(klass, name, _records):
		records = map(RecordPresenter.from_record, _records)
		return klass({
			"name": name,
			"records": records
		})

class RecordPresenter:
	def __init__(self, opts={}):
		self.alignments = opts.get("alignments")
		
	@classmethod
	def from_record(klass, record):
		alignments = map(AlignmentPresenter.from_alignment, record.alignments)
		return klass({
			"alignments" : alignments
		})

class AlignmentPresenter:
	def __init__(self, opts={}):
		self.name = opts.get("name")
		self.evalue = opts.get("evalue")
		self.start = opts.get("start")
		self.end = opts.get("end")
		self.hsps = opts.get("hsps")

	@classmethod
	def from_alignment(klass, align):
		hsps = map(HSPPresenter.from_hsp, align.hsps)
		return klass({
			"name": align.title,
			"evalue": hsps[0].evalue,
			"start": min(h.start for h in hsps),
			"end": max(h.end for h in hsps),
			"hsps": hsps
		})

class HSPPresenter:
	def __init__(self, opts={}):
		self.score = opts.get("score")
		self.start = opts.get("start")
		self.end = opts.get("end")
		self.evalue = opts.get("evalue")
		
	@classmethod
	def from_hsp(klass, hsp):
		return klass({
			"score": hsp.score,
			"start": hsp.query_start,
			"end": hsp.query_end,
			"evalue": hsp.expect
		})
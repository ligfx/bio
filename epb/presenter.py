class OrganismPresenter:
	def __init__(self, opts={}):
		self.name = opts.get("name")
		self.alignments = opts.get("alignments")
		
	@classmethod
	def from_name_and_record(klass, name, record):
		return klass({
			"name": name,
			"alignments": [AlignmentPresenter.from_alignment(a) for a in record.alignments]
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
		hsps = [HSPPresenter.from_hsp(h) for h in align.hsps]
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
class NamePresenter:
	def __init__(self, database, taxon="", extra=""):
		self.database = database
		self.taxon = taxon
		self.extra = extra

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
		self.width = opts.get("width")
		
	@classmethod
	def from_record(klass, record):
		alignments = map(AlignmentPresenter.from_alignment, record.alignments)
		return klass({
			"alignments" : alignments,
			"width" : record.query_length
		})

class AlignmentPresenter:
	def __init__(self, opts={}):
		self.name = opts.get("name")
		self.evalue = opts.get("evalue")
		self.start = opts.get("start")
		self.end = opts.get("end")
		self.width = opts.get("width")
		self.hsps = opts.get("hsps")

	@classmethod
	def from_alignment(klass, align):
		hsps = map(HSPPresenter.from_hsp, align.hsps)
		start = min(h.start for h in hsps)
		end = max(h.end for h in hsps)
		return klass({
			"name": align.title,
			"evalue": hsps[0].evalue,
			"start": start,
			"end": end,
			"width": end - start,
			"hsps": hsps
		})

class HSPPresenter:
	def __init__(self, opts={}):
		self.score = opts.get("score")
		self.strength = opts.get("strength")
		self.start = opts.get("start")
		self.end = opts.get("end")
		self.width = opts.get("width")
		self.evalue = opts.get("evalue")
	
	@classmethod
	def _score_to_strength(klass, score):
		if score < 40:
			strength = "poor"
		elif score < 50:
			strength = "fair"
		elif score < 80:
			strength = "okay"
		elif score < 200:
			strength = "good"
		elif score >= 200:
			strength = "great"
		else:
			strength = ""
		return strength
	
	@classmethod
	def from_hsp(klass, hsp):
		start = hsp.query_start
		end = hsp.query_end
		return klass({
			"score": hsp.score,
			"strength": klass._score_to_strength(hsp.score),
			"start": hsp.query_start,
			"end": hsp.query_end,
			"width": end - start,
			"evalue": hsp.expect
		})
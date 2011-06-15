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
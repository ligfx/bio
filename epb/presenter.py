class NamePresenter:
	def __init__(self, database, taxon="", extra=""):
		self.database = database
		self.taxon = taxon
		self.extra = extra
		
	def __repr__(self):
		"<NamePresenter @name={0}".format(repr((self.database, self.taxon, self.extra)))

class RecordPresenter:
	def __init__(self, record, opts={}):
		self.offset = opts["offset"]
		self.width = record.query_length
		
	def __repr__(self):
		"<RecordPresenter @width={0}, @offset={1}>".format(self.width, self.offset)

class AlignmentPresenter:
	def __init__(self, align):
		hsps = map(HSPPresenter, align.hsps)
		start = min(h.start for h in hsps)
		end = max(h.end for h in hsps)
		
		self.name = align.title
		self.evalue = hsps[0].evalue
		self.start = start
	 	self.end = end
		self.width = end - start
	
	def __repr__(self):
		"<AlignmentPresenter @name=\"{0}\">".format(self.name)

class HSPPresenter:
	def __init__(self, hsp):
		start = hsp.query_start
		end = hsp.query_end

		self.score = hsp.score
		self.strength = self.__class__._score_to_strength(hsp.score)
		self.start = hsp.query_start
		self.end = hsp.query_end
		self.width = end - start
		self.evalue = hsp.expect
	
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
class Organism:
	def __init__(self, name, matches):
		self.name = name
		self.matches = matches

class OrganismMatch:
	def __init__(self, name, seq, hsp):
		self.name = name
		
		if hsp.score < 40:
			self.strength = "poor"
		elif hsp.score < 50:
			self.strength = "fair"
		elif hsp.score < 80:
			self.strength = "okay"
		elif hsp.score < 200:
			self.strength = "good"
		elif hsp.score >= 200:
			self.strength = "great"
		else:
			self.strength = ""
		
		self.start = "%s%%" % (hsp.query_start / len(seq) * 100)
		self.width = "%s%%" % ((hsp.query_end - hsp.query_start) / len(seq) * 100)
		
		self.evalue = hsp.expect

class OrganismName:
	def __init__(self, database, taxon, extra=""):
		self.database = database
		self.taxon = taxon
		self.extra = extra
from epb import Organism, OrganismMatch
import unittest2

class TestOrganism(unittest2.TestCase):
	def test_has_properties(self):
		o = Organism("name", ["matches"])
		self.assertEqual(o.name, "name")
		self.assertEqual(o.matches, ["matches"])

class TestOrganismMatch(unittest2.TestCase):
	class HSPMock:
		def __init__(self):
			self.score = 0
			self.query_start = 5
			self.query_end = 6
			self.expect = 0
	
	def test_takes_hsp(self):
		hsp = TestOrganismMatch.HSPMock()
		m = OrganismMatch("name", "ABA", hsp)
		
		for prop in ("name", "strength", "start", "width", "evalue"):
			getattr(m, prop)
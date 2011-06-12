from epb import Organism, OrganismMatch, OrganismName
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
	
	def test_has_properties(self):
		hsp = TestOrganismMatch.HSPMock()
		m = OrganismMatch("name", "ABA", hsp)
		
		for prop in ("name", "strength", "start", "width", "evalue"):
			getattr(m, prop)
	
class TestOrganismName(unittest2.TestCase):
	def test_init(self):
		n = OrganismName("database", "taxon", "extra")
		self.assertEqual(n.database, "database")
		self.assertEqual(n.taxon, "taxon")
		self.assertEqual(n.extra, "extra")
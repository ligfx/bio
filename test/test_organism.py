from epb import Organism
import unittest2

class TestOrganism(unittest2.TestCase):
	def test_has_properties(self):
		o = Organism("name", ["matches"])
		self.assertEqual(o.name, "name")
		self.assertEqual(o.matches, ["matches"])
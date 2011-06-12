from epb import TaxonFileCollection, TaxonFileError, TaxonFileParser
from os import path
from StringIO import StringIO
import unittest2

class TestTaxonFileCollection(unittest2.TestCase):
	def setUp(self):
		self.assets = path.dirname(__file__)
		self.t = TaxonFileCollection(self.assets)
	
	def test_open(self):
		taxon = self.t.find("test")
		self.assertEqual(taxon, path.join(self.assets, "Taxon_test.txt"))

	def test_not_found(self):
		self.assertRaises(TaxonFileError, self.t.find, "nosuchfile")

class TestTaxonFileParser(unittest2.TestCase):
	def test_parse(self):
		s = "Bob\tRobert\tRobinson\nGeorgie\tPorgie\tPudding and Pie\nJohn\tSmith"
		io = StringIO(s)
		
		names = list(TaxonFileParser.parse(io))
		self.assertEqual(len(names), 3)
		self.assertEqual(names[0], ["Bob", "Robert", "Robinson"])
		self.assertEqual(names[1], ["Georgie", "Porgie", "Pudding and Pie"])
		self.assertEqual(names[2], ["John", "Smith"])
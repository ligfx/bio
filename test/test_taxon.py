from epb import TaxonFileCollection, TaxonFileError, TaxonFileParser
from os import path
import unittest2

class AbstractTaxonTestCase:
	def assets_dir(self): return path.dirname(__file__)
	def test_name(self): return "test"
	def test_file(self): return path.join(self.assets_dir(), "Taxon_%s.txt" % self.test_name())
	def bad_name(self): return "nosuchfile"

	def match_names(self, names):
		self.assertEqual(len(names), 3)
		self.assertEqual(names[0], ["Bob", "Robert", "Robinson"])
		self.assertEqual(names[1], ["Georgie", "Porgie", "Pudding and Pie"])
		self.assertEqual(names[2], ["John", "Smith"])

class TestTaxonFileCollection(unittest2.TestCase, AbstractTaxonTestCase):
	def setUp(self):
		self.t = TaxonFileCollection(self.assets_dir())
	
	def test_find(self):
		taxon = self.t.find(self.test_name())
		self.assertEqual(taxon, self.test_file())
		
	def test_find_raises(self):
		self.assertRaises(TaxonFileError, self.t.find, self.bad_name())
		
	def test_parse(self):
		names = list(self.t.parse(self.test_name()))
		self.match_names(names)

class TestTaxonFileParser(unittest2.TestCase, AbstractTaxonTestCase):
	def test_parse(self):
		with open(self.test_file()) as f:
			names = list(TaxonFileParser.parse(f))
			self.match_names(names)
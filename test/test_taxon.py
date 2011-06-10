from epb import TaxonFileParser
from StringIO import StringIO
import unittest2

class TestTaxonFileParser(unittest2.TestCase):
	def test_parse(self):
		s = "Bob\tRobert\tRobinson\nGeorgie\tPorgie\tPudding and Pie\nJohn\tSmith"
		io = StringIO(s)
		
		names = list(TaxonFileParser.parse(io))
		self.assertEqual(len(names), 3)
		self.assertEqual(names[0], ["Bob", "Robert", "Robinson"])
		self.assertEqual(names[1], ["Georgie", "Porgie", "Pudding and Pie"])
		self.assertEqual(names[2], ["John", "Smith"])
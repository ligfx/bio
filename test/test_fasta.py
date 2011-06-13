from epb import Fasta
import unittest2

class TestFasta(unittest2.TestCase):
	def test_normalize(self):
		sequences = """
> Name1
Bo
dy

> Name2
yd

oB
		"""
		want = "BodyydoB"
		
		normal = Fasta.normalize(sequences)
		self.assertEqual(normal, want, "incorrect normalized form")
		
	def test_each(self):
		sequences = """
> Bob the [Builder]
Bob Robinson
> George
George Harrison
		"""
		
		each = list(Fasta.each(sequences))
		self.assertEqual(len(each), 2, "incorrect length")
		
		self.assertEqual(each[0].name, "Bob the [Builder]")
		self.assertEqual(each[0].seq, "BobRobinson")
		self.assertEqual(each[0].size, 11)
		
		self.assertEqual(each[1].name, "George")
		self.assertEqual(each[1].seq, "GeorgeHarrison")
		self.assertEqual(each[1].size, 14)
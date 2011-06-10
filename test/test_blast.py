from epb import Blaster
import unittest2

class TestBlast(unittest2.TestCase):
	def test_fails_without_seq(self):
		self.assertRaises(TypeError, list, Blaster.blast, seq="")
	
	def test_fails_without_db(self):
		self.assertRaises(TypeError, list, Blaster.blast, db="")
		
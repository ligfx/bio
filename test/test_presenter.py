from epb import HSPPresenter
import unittest2

class HSPMock:
	def __init__(self):
		self.score = 0
		self.query_start = 5
		self.query_end = 6
		self.expect = 0

class TestHSPPresenter(unittest2.TestCase):
	def test_from_hsp(self):
		m = HSPMock()
		h = HSPPresenter.from_hsp(m)
		
		self.assertEqual(h.score, 0)
		self.assertEqual(h.start, 5)
		self.assertEqual(h.end, 6)
		self.assertEqual(h.evalue, 0)
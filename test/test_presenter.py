from epb import AlignmentPresenter, HSPPresenter
import unittest2

class AlignmentMock:
	def __init__(self):
		self.title = "name"
		self.hsps = [HSPMock().one(), HSPMock().two()]

class HSPMock:
	def one(self):
		self.score = 0
		self.query_start = 5
		self.query_end = 6
		self.expect = 0
		return self
	
	def two(self):
		self.score = 1
		self.query_start = 6
		self.query_end = 8
		self.expect = 0
		return self

class TestAlignmentPresenter(unittest2.TestCase):
	def test_from_hit(self):
		m = AlignmentMock()
		h = AlignmentPresenter.from_alignment(m)
		
		self.assertEqual(h.name, "name")
		self.assertEqual(h.evalue, 0)
		self.assertEqual(h.start, 5)
		self.assertEqual(h.end, 8)
		self.assertEqual(len(h.hsps), 2)

class TestHSPPresenter(unittest2.TestCase):
	def test_from_hsp(self):
		m = HSPMock().one()
		h = HSPPresenter.from_hsp(m)
		
		self.assertEqual(h.score, 0)
		self.assertEqual(h.start, 5)
		self.assertEqual(h.end, 6)
		self.assertEqual(h.evalue, 0)
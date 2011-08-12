# [Back to docs.py](docs.html)

from itertools import groupby

# === DataSet ===

# Interface for working with &ldquo;rows&rdquo; of data.
class DataSet:
	# Each item in `data` is assumed to be an object of the form
	#
	#     {
	#       "record": ...,
	#       "alignment": ...,
	#       "hsp": ...
	#     }
	def __init__(self, data):
		self.data = list(data)
	
	# === by_record ===
	def by_record(self):
		return self._group('record')

	# === by_alignment ===
	def by_alignment(self):
		data = self._group('alignment')
		data.sort(key=lambda (a, d): d.minimum_evalue())
		return data
	
	# === by_hsp ===
	
	# Unlike the other grouping functions, `by_hsp` returns a single datum, not a whole `DataSet`.
	def by_hsp(self):
		data = self._group('hsp')
		return [(hsp, next(iter(d))) for (hsp, d) in data]
	
	# === minimum_evalue ===
	def minimum_evalue(self):
		return min(d['hsp'].evalue for d in self.data)
		
	# === minimum_subject_start ===
	def minimum_subject_start(self):
		return min(d['hsp'].subject_start for d in self.data)
		
	# === maximum_subject_end ===
	def maximum_subject_end(self):
		return max(d['hsp'].subject_end for d in self.data)
		
	# === \_\_iter__ ===
	def __iter__(self):
		return iter(self.data)
		
	def _group(self, key):
		f = lambda _: _[key]
		scope = sorted(self.data, key = f)
		groups = groupby(scope, f)
		return [(group, DataSet(data)) for (group, data) in groups]
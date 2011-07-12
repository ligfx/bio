# [Back to docs.py](docs.html)

from itertools import groupby

# === DataSet ===

# Interface for working with &ldquo;rows&rdquo; of data.
class DataSet:
	# Each item in `data` is assumed to be an object of the form
	#
	#     {
	#       "organism": ...,
	#       "record": ...,
	#       "alignment": ...,
	#       "hsp": ...
	#     }
	def __init__(self, data):
		self.data = data
	
	# === by_organism ===
	def by_organism(self):
		return self._group('organism')
	
	# === by_record ===
	def by_record(self):
		return self._group('record')

	# === by_alignment ===
	def by_alignment(self):
		data = self._group('alignment')
		data.sort(key=lambda (a, d): d.lowest_evalue())
		return data
	
	# === by_hsp ===
	
	# Unlike the other grouping functions, `by_hsp` returns a single datum, not a whole `DataSet`.
	def by_hsp(self):
		data = self._group('hsp')
		return [(hsp, next(iter(d))) for (hsp, d) in data]
	
	# === lowest_evalue ===
	def lowest_evalue(self):
		return min(d['hsp'].evalue for d in self.data)
		
	# === \_\_iter__ ===
	def __iter__(self):
		return iter(self.data)
		
	def _group(self, key):
		f = lambda _: _[key]
		scope = sorted(self.data, key = f)
		groups = groupby(scope, f)
		return [(group, DataSet(list(data))) for (group, data) in groups]
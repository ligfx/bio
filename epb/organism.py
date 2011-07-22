# [Back to docs.py](docs.html)

import epb.blast as Blast
from epb.data import DataSet
import os
import yaml

# === OrganismCollection ===
class OrganismCollection:
	ext = ".info"

	def __init__(self, path, organisms):
		self.path = path
		self.organisms = organisms
		
	def __len__(self):
		return len(self.organisms)

	# === blast ===
	def blast(self, sequence, **opts):
		
		callback = opts.get("callback", None)
		
		data = []
		
		for (organism, info) in self.organisms.items():
			if callback: callback(organism)
			xml = Blast.get_xml(os.path.join(self.path, organism), sequence)
			
			for datum in Blast.parse_xml(xml):
				datum['organism'] = info.get('name', organism)
				data.append(datum)
		
		return DataSet(data)

	# === find_all_by_categories ===
	@classmethod
	def find_all_by_categories(klass, categories, **opts):
		path = opts['path']
		categories = [c.lower() for c in categories]

		info_files = [f for f in os.listdir(path) if f.endswith(klass.ext)]

		organism_names = {}

		for fname in info_files:
			with open(os.path.join(path, fname)) as f:
				info = yaml.load(f) or {}
				if True: #any((c.strip().lower() in categories) for c in info_categories):
					name = fname[:-len(klass.ext)]
					import sys
					organism_names[name] = info

		return OrganismCollection(path, organism_names)

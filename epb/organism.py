# [Back to docs.py](docs.html)

import epb.blast as Blast
from epb.data import DataSet
import os
import re
import yaml

# === Organism ===
class Organism:
	def __init__(self, path, slug, info):
		self.path = path
		self.slug = slug
		self.info = info
		self.name = info.get('name', slug)
		
	def url_for_gene(self, gene):
		match = re.match(self.info.get('fasta_header_format', ''), gene)
		if match:
			keys = match.groupdict()
			for k in keys:
				if keys[k]:
					keys[k] = keys[k].strip()
		else:
			keys = {}
		return self.info.get('gene_url','#').format(**keys)

# === OrganismCollection ===
class OrganismCollection:
	ext = ".info"

	def __init__(self, organisms):
		self.organisms = organisms
		
	def __len__(self):
		return len(self.organisms)

	# === blast ===
	def blast(self, sequence, **opts):
		
		callback = opts.get("callback", None)
		
		data = []
		
		for organism in self.organisms:
			if callback: callback(organism)
			xml = Blast.get_xml(os.path.join(organism.path, organism.slug), sequence)
			
			for datum in Blast.parse_xml(xml):
				datum['organism'] = organism
				data.append(datum)
		
		return DataSet(data)

	# === find_all_by_categories ===
	@classmethod
	def find_all_by_categories(klass, categories, **opts):
		path = opts['path']
		categories = [c.lower() for c in categories]

		info_files = [f for f in os.listdir(path) if f.endswith(klass.ext)]

		organisms = []

		for fname in info_files:
			with open(os.path.join(path, fname)) as f:
				info = yaml.load(f) or {}
				if True: #any((c.strip().lower() in categories) for c in info_categories):
					slug = fname[:-len(klass.ext)]
					organisms.append(Organism(path, slug, info))

		return OrganismCollection(organisms)

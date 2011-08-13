# [Back to docs.py](docs.html)

import epb.blast as Blast
from epb.data import DataSet
import os
import re
import sqlite3
import yaml

class Domain:
	def __init__(self, row):
		self.id = row[0]
		self.accession = row[1]
		self.name = row[2]
		self.accession_name = row[3]
		self.evalue = row[4]
		self.query_start = row[5]
		self.query_end = row[6]
		self.dlength = row[7]
		self.dstart = row[8]
		self.dend = row[9]
		
		self.url = "http://pfam.sanger.ac.uk/family/" + self.accession_name

class OrganismDatabase:
	class Guard:
		def in_order(self, f1, f2):
			f1(); f2()
	
	file_ext = ".db"
	
	def __init__(self, dbdir, slug):
		self.path = os.path.join(dbdir, slug) + self.file_ext
	
	def cursor(self):
		try:
			conn = sqlite3.connect(self.path)
			c = conn.cursor()
			guard = OrganismDatabase.Guard()
			guard.__enter__ = lambda: c
			guard.__exit__ = lambda *args: guard.in_order(c.close, conn.close)
			return guard
		except:
			raise Exception("Problem with database {}".format(self.path))
	
	def get_sequence(self, alignment):
		with self.cursor() as c:
			statement = c.execute('select sequences.sequence from sequences where sequences.accession = ? limit 1', (alignment,))
			row = statement.fetchone()
			if not row:
				statement = c.execute('select sequences.sequence from sequences where sequences.fullname = ? limit 1', (alignment,))
				row = statement.fetchone()
			return row[0]

	def get_domains(self, alignment):
		with self.cursor() as c:
			statement = c.execute('select domains.* from domains where domains.accession = ?', (alignment,))
			return list(map(Domain, statement.fetchall()))

	def get_fullname(self, alignment):
		with self.cursor() as c:
			statement = c.execute('select sequences.fullname from sequences where sequences.accession = ? limit 1', (alignment,))
			row = statement.fetchone()
			if row:
				return row[0]
			else:
				return alignment

# === Organism ===
class Organism:
	def __init__(self, slug, info, **kwargs):
		self.slug = slug
		self.info = info
		
		self.blastdir = kwargs['blastdir']
		
		self.name = info.get('name', slug)
		self.database = OrganismDatabase(kwargs['dbdir'], slug)
		
		self.blast_data = None
		
	def blast(self, sequence, opts):
		if self.blast_data: return self.blast_data
		
		xml = Blast.get_xml(os.path.join(self.blastdir, self.slug), sequence, opts)
		self.blast_data = DataSet(list(Blast.parse_xml(xml)))
		return self.blast_data
		
	def url_for_gene(self, gene):
		format = self.info.get('fasta_header_format', '')
		url = self.info.get('gene_url', '#')
		
		if not format and "{" in url:
			return "#BAD-KEY:fasta_header_format"
		
		match = re.match(self.info.get('fasta_header_format', ''), ">" + gene)
		if match:
			keys = match.groupdict()
		else:
			return "#BAD-MATCH:fasta_header_format:%s" % gene
		
		for (k, v) in keys.items():
			url = re.sub(r"\{\s*%s\s*\}" % k, v.strip(), url)
		return url
	
	def get_sequence(self, alignment):
		return self.database.get_sequence(alignment)
		
	def get_domains(self, alignment):
		return self.database.get_domains(alignment)
		
	def get_fullname(self, alignment):
		return self.database.get_fullname(alignment)

# === OrganismCollection ===
class OrganismCollection:
	infoext = ".yaml"
	
	blastdir = None
	dbdir = None
	infodir = None
	listdir = None

	# === find_all_by_categories ===
	@classmethod
	def find_all_by_categories(klass, categories):
		
		organism_slugs = []
		for category in categories:
			with open(os.path.join(klass.listdir, category)) as f:
				for line in f:
					organism_slugs.append(line.strip())
		
		organisms = []
		for slug in organism_slugs:
			with open(os.path.join(klass.infodir, slug) + klass.infoext) as f:
				info = yaml.load(f) or {}
				organisms.append(
					Organism(slug, info,
					blastdir = klass.blastdir,
					dbdir = klass.dbdir)
				)

		return organisms

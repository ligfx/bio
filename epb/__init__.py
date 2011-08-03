from os import path
import yaml

import epb.controller
import epb.fasta as Fasta
from epb.organism import *
from epb.presenter import *

class config:
	def __init__(self, directory=path.dirname(__file__)):
		self.directory = directory
		self.configfile = path.join(self.directory, 'config.yaml')
		with open(self.configfile) as f:
			self.config = yaml.load(f)
		self.blast_dir = self.absolute_directory(self.config['blast_dir'])
		self.db_dir = self.absolute_directory(self.config['db_dir'])
		self.info_dir = self.absolute_directory(self.config['info_dir'])
		self.results_output_dir = self.absolute_directory(self.config['results_output_dir'])
		self.results_http_dir = self.config['results_http_dir']
	
	def absolute_directory(self, directory):
		if directory.startswith("/"):
			return directory
		else:
			return path.join(self.directory, directory)

import sys
if __file__ == sys.argv[0]:
	method = sys.argv[1]
	categories = sys.argv[2:]
	sequence = sys.stdin.read()
	
	e = config()
	sys.stderr.write("[debug] configfile: %s\n" % e.configfile)
	sys.stderr.write("[debug] dbdir: %s\n" % e.dbdir)
	
	OrganismCollection.blastdir = e.blastdir
	OrganismCollection.dbdir = e.dbdir
	OrganismCollection.infodir = e.infodir
	
	organisms = OrganismCollection.find_all_by_categories(categories)
	seq = Fasta.normalize(sequence, method=method)
	data = organisms.blast(seq, callback=lambda organism: sys.stderr.write("[debug] Blasting %s\n" % organism.name))

	sequences = Fasta.each(sequence)

	print epb.controller.results({
		"data": data,
		"sequences": sequences
	}).encode('utf-8')
	

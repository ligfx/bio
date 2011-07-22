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
		self.dbdir = self.config['dbdir']
		if not self.dbdir.startswith("/"):
			self.dbdir = path.join(self.directory, self.dbdir)

import sys
if __file__ == sys.argv[0]:
	method = sys.argv[1]
	categories = sys.argv[2:]
	sequence = sys.stdin.read()
	
	e = config()
	sys.stderr.write("[debug] configfile: %s\n" % e.configfile)
	sys.stderr.write("[debug] dbdir: %s\n" % e.dbdir)
	
	organisms = OrganismCollection.find_all_by_categories(
		categories, path=e.dbdir
	)
	seq = Fasta.normalize(sequence, method=method)
	data = organisms.blast(seq, callback=lambda organism: sys.stderr.write("[debug] Blasting %s\n" % organism))

	sequences = Fasta.each(sequence)

	print epb.controller.results({
		"data": data,
		"sequences": sequences
	}).encode('utf-8')
	

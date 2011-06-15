import jinja2
import logging
from os import path
import yaml

from epb.blast import *
from epb.cgi import *
from epb.fasta import *
from epb.organism import *
from epb.presenter import *
from epb.taxon import *

MODULEDIR = path.dirname(__file__)

class EPB:
	def __init__(self):
		logging.basicConfig(format = "%(asctime)s %(name)s: %(message)s", level=logging.DEBUG)
		self.log = logging.getLogger("epb[EPB]")
		
		configfile = path.join(MODULEDIR, 'config.yaml')
		self.log.debug("configuration: %s" % configfile)
		with open(configfile) as f:
			self.config = yaml.load(f)

		self.dbdir = self.config['dbdir']
		self.log.debug("config['dbdir']: %s" % self.dbdir)
	
	def organism_names(self, taxon):
		t = TaxonFileCollection(MODULEDIR)
		return (OrganismName(*k) for k in t.parse(taxon))
	
	def blast(self, seq, names, cb=None):
		organisms = []
		for name in names:
			if cb: cb()
			self.log.debug("blasting %s" % name.database)
			try:
				o = Organism.blast(name=name, db=path.join(self.dbdir, name.database), seq=seq)
				organisms.append(o)
			except BlastError as e:
				logging.getLogger("blastall").warning("Error: %s" % e)
		return organisms
	
	def render(self, sequences, organisms):
		env = jinja2.Environment(loader = jinja2.PackageLoader('epb', 'templates'))
		template = env.get_template('results.html.jinja2')
		
		total_sequence_width = "%f%%" % sum(float(s.width.replace('%', '')) for s in sequences[:-1])
		return template.render(organisms = organisms, sequences = sequences, total_sequence_width=total_sequence_width)
		
	def go(self, seq, taxon, cb=None):
		self.log.debug("seq: %s" % seq)
		self.log.debug("taxon: %s" % taxon)
		
		nseq = Fasta.normalize(seq)
		self.log.debug("normalized sequence: %s" % nseq)
		
		names = self.organism_names(taxon)
		results = self.blast(nseq, names, cb)
		
		seqs = list(Fasta.each(seq))
		total = len(nseq)
		p = None
		for s in seqs:
			s.width = "%f%%" % (s.size * 100.0 / total)
			s.previous, p = p, s
		
		
		return self.render(seqs, results)

import sys
if __file__ == sys.argv[0]:	
	taxon = sys.argv[1]
	seq = sys.stdin.read()
	
	e = EPB()
	print e.go(seq, taxon)
	

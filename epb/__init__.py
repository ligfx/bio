import jinja2
import logging
from os import path
import yaml

from epb.blast import *
from epb.fasta import *
from epb.organism import *
from epb.taxon import *
from epb.utils import *

MODULEDIR = path.dirname(__file__)

class EPB:
	@classmethod
	def organism_names(klass, taxon):
		t = TaxonFileCollection(MODULEDIR)
		return (OrganismName(*k) for k in t.parse(taxon))
	
	@classmethod
	def blast(klass, seq, db_dir, names):
		organisms = []
		for name in names:
			try:
				matches = []
				for record in Blaster.blast(db=path.join(db_dir, organism_name.database), seq=seq):
					for a in record.alignments:
						for hsp in a.hsps:
							matches.append(OrganismMatch(a.title, seq, hsp))
				organisms.append(Organism(name, matches))
			except BlastError as e:
				print "[Blaster] Error: %s" % e
		return organisms
	
	@classmethod
	def render(klass, organisms):
		env = jinja2.Environment(loader = jinja2.PackageLoader('epb', 'templates'))
		template = env.get_template('results.html.jinja2')
		
		return template.render(organisms = organisms)
		
	@classmethod
	def go(klass, seq, taxon, db_dir):
		log = logging.getLogger("epb.go")
		log.debug("seq=%s" % seq)
		log.debug("taxon=%s" % taxon)
		
		seq = Fasta.normalize(seq)
		names = klass.organism_names(taxon)
		results = klass.blast(seq, db_bir, names)
		return klass.render(results)

import sys
if __file__ == sys.argv[0]:
	logging.basicConfig(format = "%(asctime)s %(name)s: %(message)s", level=logging.DEBUG)
	
	taxon = sys.argv[1]
	seq = sys.stdin.read()
	
	with open(path.join(MODULEDIR, 'config.yaml')) as f:
		config = yaml.load(f)

	db_dir = config['db_dir']
	print EPB.go(seq, taxon, db_dir)
	

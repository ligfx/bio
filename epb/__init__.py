import jinja2
from os import path

from epb.blast import *
from epb.fasta import *
from epb.organism import *
from epb.taxon import *
from epb.utils import *

EPB_MODULEDIR = path.dirname(__file__)

class DatabaseCollection:
	def __init__(self, dir):
		self.dir = dir
	def find(self, name):
		return path.join(self.dir, name)

import sys
if __file__ == sys.argv[0]:
	taxon = sys.argv.pop()
	seq = Fasta.normalize(sys.stdin.read())
	
	db = DatabaseCollection("databases")
	organisms = []
	for organism_name in OrganismName.find_all_by_taxonomy(taxon):
		try:
			matches = []
			for record in Blaster.blast(db=db.find(organism_name.database), seq=seq):
				for a in record.alignments:
					for hsp in a.hsps:
						matches.append(OrganismMatch(a.title, seq, hsp))
			organisms.append(Organism(organism_name, matches))
		except BlastError as e:
			print "[Blaster] Error: %s" % e
	
	env = jinja2.Environment(loader = jinja2.PackageLoader('epb', 'templates'))
	template = env.get_template('results.html.jinja2')
	
	print template.render(organisms = organisms)
	

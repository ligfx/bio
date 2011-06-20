import jinja2
import logging
from os import path
import yaml

from epb.blast import *
from epb.cgi import *
from epb.fasta import *
from epb.presenter import *
from epb.taxon import *

MODULEDIR = path.dirname(__file__)

class Controller:
	def __init__(self, params={}):
		self.params = params
		self.dbdir = self.params['dbdir']
		self.logger = logging.getLogger("epb[Controller]")

	def log(self, msg):
		self.logger.debug(msg)
		
	def results(self):
		# We've got three different pathways here
		# 1) We have one sequence. Easy, just blast it and render it
		# 2) We have multiple sequences, concatenated. Blast the concatenated
		#    sequence, but give the renderer each individual sequence (so we can
		#    see the boundaries)
		# 3) We have multiple sequences, separate. Blast the sequences, and for each
		#    record add an offset (erm? I have qualms about this), then render them like before
		
		names = self.params["names"]
		fasta = self.params["sequence"]
		method = self.params["method"] # 'concat' || 'multiple'
		
		if method == 'concat':
			seq = Fasta.normalize(fasta)
		elif method == 'multiple':
			seq = fasta
		else:
			raise Exception, "method must be one of 'concat' or 'multiple'"
		
		organisms = []
		for name in names:
			self.log("blasting %s" % name.database)
			try:
				records = Blaster.blast(seq=seq, db=path.join(self.dbdir, name.database))
				organisms.append(OrganismPresenter.from_name_and_records(name, records))
			except BlastError as e:
				logging.getLogger("blastall").warning("Error: %s" % e)
		
		sequences = list(Fasta.each(fasta))
		
		return self.render("results", {
			"organisms": organisms,
			"sequences": sequences
		})
		
	def render(self, action, context):
		env = jinja2.Environment(loader = jinja2.PackageLoader('epb', 'templates'))
		env.filters['as_percent'] = lambda value, total: "{0}%".format(value * 100.0 / total)
		env.filters['sum_attr'] = lambda enum, attr: sum(getattr(e, attr) for e in enum)
		
		template = env.get_template("%s.html.jinja2" % action)

		context['input_width'] = sum(s.size for s in context['sequences'])
		
		for o in context['organisms']:
			offset = 0
			for r in o.records:
				r.offset = offset
				offset += r.width

		return template.render(context)

class EPB:
	def __init__(self):
		logging.basicConfig(format = "%(asctime)s %(name)s: %(message)s", level=logging.DEBUG)
		self.log = logging.getLogger("epb[EPB]")
		
		configfile = path.join(MODULEDIR, 'config.yaml')
		self.log.debug("configuration: %s" % configfile)
		with open(configfile) as f: self.config = yaml.load(f)

		self.dbdir = self.config['dbdir']
		self.log.debug("config['dbdir']: %s" % self.dbdir)
		
		self.taxons = TaxonFileCollection(MODULEDIR)
		self.log.debug("taxons: %s" % self.taxons)
	
	def dispatch(self, params={}):
		taxon = params['taxon']
		params['names'] = [NamePresenter(*k) for k in self.taxons.parse(params['taxon'])]
		params['dbdir'] = self.dbdir
		c = Controller(params)
		return c.results()

import sys
if __file__ == sys.argv[0]:	
	taxon = sys.argv[1]
	method = sys.argv[2]
	seq = sys.stdin.read()
	
	e = EPB()
	print e.dispatch({
		"sequence": seq,
		"method": method,
		"taxon":taxon
	})
	

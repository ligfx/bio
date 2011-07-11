from itertools import groupby
import jinja2
import logging
from os import path
import yaml

from epb.blast import *
from epb.cgi import *
import epb.fasta as Fasta
from epb.presenter import *
from epb.taxon import *

MODULEDIR = path.dirname(__file__)

class Controller:
	def __init__(self, params={}):
		self.params = params
		self.blast = Blast({"database_path": params['dbdir']})
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
		
		data = self.blast.find_all(seq, names)
		sequences = list(Fasta.each(fasta))
		
		return self.render("results", {
			"data": data,
			"sequences": sequences
		})
		
	def render(self, action, context):
		env = jinja2.Environment(loader = jinja2.PackageLoader('epb', 'templates'))
		env.filters['as_percent'] = lambda value, total: "{0}%".format(value * 100.0 / total)
		env.filters['map_function'] = lambda enum, name: (eval(name)(e) for e in enum)
		
		template = env.get_template("%s.html.jinja2" % action)

		context['input_width'] = sum(len(s) for s in context['sequences'])
		context['render'] = lambda r: env.get_template("%s" % r).render(context)

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
		
		self.taxons = TaxonFileCollection(path.join(MODULEDIR, 'taxons'))
		self.log.debug("taxons: %s" % self.taxons)
	
	def dispatch(self, params={}):
		taxon = params['taxon']
		params['names'] = (NamePresenter(*k) for k in self.taxons.parse(params['taxon']))
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
	

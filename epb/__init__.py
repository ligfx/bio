from os import path
import yaml

import epb.controller as Controller
from epb.presenter import *
from epb.taxon import *

class EPB:
	def __init__(self, directory):
		self.directory = directory
		self.configfile = path.join(self.directory, 'config.yaml')
		with open(self.configfile) as f:
			self.config = yaml.load(f)
		self.dbdir = self.config['dbdir']
		self.taxons = TaxonFileCollection(path.join(self.directory, 'taxons'))
	
	def dispatch(self, params={}):
		params['names'] = (NamePresenter(*k) for k in self.taxons.parse(params['taxon']))
		params['dbdir'] = self.dbdir
		return Controller.results(params)

import sys
if __file__ == sys.argv[0]:	
	taxon = sys.argv[1]
	method = sys.argv[2]
	seq = sys.stdin.read()
	
	e = EPB(path.dirname(__file__))
	sys.stderr.write("[debug] configfile: %s\n" % e.configfile)
	sys.stderr.write("[debug] dbdir: %s\n" % e.dbdir)
	sys.stderr.write("[debug] taxons: %s\n" % e.taxons.dir)
	print e.dispatch({
		"sequence": seq,
		"method": method,
		"taxon":taxon
	})
	

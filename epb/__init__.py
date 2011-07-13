from os import path
import yaml

import epb.controller as Controller
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
	
	def dispatch(self, params={}):
		params['dbdir'] = self.dbdir
		return Controller.results(params)

import sys
if __file__ == sys.argv[0]:
	method = sys.argv[1]
	categories = sys.argv[2:]
	seq = sys.stdin.read()
	
	e = EPB(path.dirname(__file__))
	sys.stderr.write("[debug] configfile: %s\n" % e.configfile)
	sys.stderr.write("[debug] dbdir: %s\n" % e.dbdir)
	print e.dispatch({
		"sequence": seq,
		"method": method,
		"categories": categories
	})
	

#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import epb
import epb.controller
import epb.fasta as Fasta
from epb.organism import OrganismCollection
import epb.web
import time
import traceback

import cgi

try:

	request = epb.web.Request()
	if any(request.missing):
		print "Status: 400 Bad Request"
		print "Content-Type: text/html"
		print
		print epb.controller.status({
			"done": True,
			"error": "<p>Missing parameter(s) '%s'. Please fix the problem, or contact the webmaster if this keeps happening.</p>" % (", ".join(request.missing))
		})
		exit(0)
	
	job = epb.web.Job()
	config = epb.config()

	organisms = OrganismCollection.find_all_by_categories(
		request.categories, path=config.dbdir
	)

	status = {"job": job.id, "steps": [], "organisms": organisms}
	with job.status_file() as f:
		f.write(epb.controller.status(status))

	print "Status: 302 Found"
	print "Location: %s" % job.status_file_path
	print "Content-Type: text/plain"
	print
	#print status_file
	print
	
except Exception:
	print "Status: 500 Internal Server Error"
	print "Content-Type: text/html"
	print
	print epb.controller.status({
		"done": True,
		"error": "<pre>%s</pre>" % cgi.escape(traceback.format_exc())
	})
	exit(0)

sys.stdout.flush()

if os.fork(): exit(0)

sys.stdin.close()
sys.stdout.close()
sys.stderr.close()

os.close(0)
os.close(1)
os.close(2)

try:

	def callback(organism):
		global status
		status['steps'] = ["Blasting %s" % organism] + status['steps']
		
		with job.status_file() as f:
			f.write(epb.controller.status(status))

	seq = Fasta.normalize(request.sequence, method=request.method)
	data = organisms.blast(seq, callback=callback)

	sequences = Fasta.each(request.sequence)

	results = epb.controller.results({
		"data": data,
		"sequences": sequences
	})

	status['done'] = True
	with job.status_file() as f:
		f.write(epb.controller.status(status))

	with job.results_file() as f:
		f.write(results)

except:
	status['done'] = True
	status['error'] = "<pre>%s</pre>" % cgi.escape(traceback.format_exc())
	
	with job.status_file() as f:
		f.write(epb.controller.status(status))
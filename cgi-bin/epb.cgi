#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import epb
import epb.controller
import epb.fasta as Fasta
from epb.organism import OrganismCollection
import time
import traceback

import cgi

def missing_param(param):
	print "Status: 400 Bad Request"
	print "Content-Type: text/html"
	print
	print epb.controller.status({
		"done": True,
		"error": "<p>Missing parameter '%s'. Please fix the problem, or contact the webmaster if this keeps happening.</p>" % param
	})
	
	exit(0)

class Request:
	def __init__(self):
		form = cgi.FieldStorage()
		
		self.sequence = form.getvalue("sequence", None)
		if not self.sequence: missing_param('sequence')
		self.method = form.getvalue("method", None)
		if not self.method: missing_param('method')
		self.categories = form.getlist("category")
		if not self.categories: missing_param('category')

class Job:
	_directory = "results"
	
	def __init__(self):
		self.id = int(time.time())
		# Shard the results into different folders, so we don't run into
		# issues with directory size limits
		shard = ("%06i" % (self.id % 999999))
		self.shard = os.path.join(shard[:3], shard[3:])
		
		self.output_directory = os.path.join(self._directory, self.shard, str(self.id))
		os.makedirs(self.output_directory)

		self.status_file = os.path.join(self.output_directory, "status.html")
		self.status_file_temp = self.status_file + "_temp"
		
		self.results_file = os.path.join(self.output_directory, "results.html")

try:

	directory = "results"

	request = Request()
	job = Job()

	status = {"job": job.id, "steps": []}
	with open(job.status_file, "w") as f:
		f.write(epb.controller.status(status))

	print "Status: 302 Found"
	print "Location: %s" % job.status_file
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

	e = epb.EPB(os.path.dirname(epb.__file__))

	def callback(organism):
		global status
		status['steps'] = ["Blasting %s" % organism] + status['steps']
		with open(job.status_file_temp, "w") as f:
			f.write(epb.controller.status(status))
		os.rename(job.status_file_temp, job.status_file)

	if request.method == 'concat':
		seq = Fasta.normalize(request.sequence)
	elif request.method == 'multiple':
		seq = request.sequence
	else:
		raise Exception, "method must be one of 'concat' or 'multiple'"

	organisms = OrganismCollection.find_all_by_categories(
		request.categories, path=e.dbdir
	)
	data = organisms.blast(seq, callback=callback)

	sequences = list(Fasta.each(request.sequence))

	results = epb.controller.results(data=data, sequences=sequences)

	status['done'] = True
	with open(job.status_file_temp, "w") as f:
		f.write(epb.controller.status(status))
	os.rename(job.status_file_temp, job.status_file)

	with open(job.results_file, "w") as f:
		f.write(results)

except:
	status['done'] = True
	status['error'] = "<pre>%s</pre>" % cgi.escape(traceback.format_exc())
	
	with open(job.status_file, "w") as f:
		f.write(epb.controller.status(status))
	os.rename(job.status_file_temp, job.status_file)
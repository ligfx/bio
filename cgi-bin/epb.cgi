#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import epb
import epb.render
import epb.fasta as Fasta
from epb.domains import PfamScan
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
		print epb.render.status({
			"done": True,
			"error": "<p>Missing parameter(s) '%s'. Please fix the problem, or contact the webmaster if this keeps happening.</p>" % (", ".join(request.missing))
		})
		exit(0)
	
	config = epb.config(os.path.dirname(__file__))
	job = epb.web.Job(config.results_output_dir, config.results_http_dir)

	OrganismCollection.blastdir = config.blast_dir
	OrganismCollection.dbdir = config.db_dir
	OrganismCollection.infodir = config.info_dir
	OrganismCollection.listdir = config.organism_lists_dir

	organisms = OrganismCollection.find_all_by_categories(request.categories)

	status = {"job": job.id, "steps": [], "organisms": organisms}
	with job.status_file() as f:
		f.write(epb.render.status(status))

	print "Status: 302 Found"
	print "Location: %s" % job.status_http_path
	print "Content-Type: text/plain"
	print
	
except Exception:
	print "Status: 500 Internal Server Error"
	print "Content-Type: text/html"
	print
	print epb.render.status({
		"done": True,
		"error": "<pre>%s</pre>" % cgi.escape(traceback.format_exc())
	})
	exit(0)

# Disconnect from the server by forking and closing all input/output pipes
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
		status['steps'] = ["Blasting %s" % organism.name] + status['steps']
		
		with job.status_file() as f:
			f.write(epb.render.status(status))

	seq = Fasta.normalize(request.sequence, method=request.method)
	data = organisms.blast(seq, callback=callback, evalue=request.evalue)
	
	PfamScan.pfamdir = config['pfam_dir']
	domains = PfamScan.get_domains(seq)
	
	sequences = Fasta.each(request.sequence)

	results = epb.render.results({
		"data": data,
		"domains": domains,
		"sequences": sequences
	})

	with job.results_file() as f:
		f.write(results.encode('utf-8'))
		
	for organism, data in data.by_organism():
		for alignment, data in data.by_alignment():
			html = epb.render.alignment({
				"data": data,
				"alignment": alignment,
				"organism": organism
			})
			with job.alignment_file(alignment.digest) as f:
				f.write(html.encode('utf-8'))

	status['done'] = True
	with job.status_file() as f:
		f.write(epb.render.status(status))

except:
	status['done'] = True
	status['error'] = "<pre>%s</pre>" % cgi.escape(traceback.format_exc())
	
	with job.status_file() as f:
		f.write(epb.render.status(status))
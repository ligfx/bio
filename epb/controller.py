# [Back to docs.py](docs.html)

import jinja2

import epb.fasta as Fasta
from epb.organism import OrganismCollection
import os
import yaml

# === status ===

# Renders job status page
def status(params):
	return render("status.html.jinja2", params)

# === results ===

# Renders results page.
#
# `params` is expected to be of the form
#
#     {
#       "names": [NamePresenter],
#       "sequence": string,
#       "method": "concat" or "multiple",
#       "dbdir": string
#     }
#
# We have three different pathways here:
#
# 1. We have one sequence. Easy, just blast it and render it
# 2. We have multiple sequences, concatenated. Blast the concatenated
#    sequence, but give the renderer each individual sequence (so we can
#    see the boundaries)
# 3. We have multiple sequences, separate. Blast the sequences, and for each
#    record add an offset (erm? I have qualms about this), then render them like before
def results(**opts):
	data = opts['data']
	sequences = opts['sequences']
	
	return render("results.html.jinja2", {
		"data": data,
		"sequences": sequences,
		"input_width": sum(len(s) for s in sequences)
	})

# === render ===

# Render [Jinja2](http://jinja.pocoo.org/docs/) template from directory `epb/templates`
def render(action, context={}):
	template = environment().get_template(action)
	return template.render(context)

def environment():
	env = jinja2.Environment(
		loader = jinja2.PackageLoader('epb', 'templates'),
		extensions = ['jinja2.ext.with_']
	)
	env.filters['as_percent'] = lambda value, total: "{0}%".format(value * 100.0 / total)
	env.filters['map_function'] = lambda enum, name: (eval(name)(e) for e in enum)
	env.globals['render'] = render
	return env
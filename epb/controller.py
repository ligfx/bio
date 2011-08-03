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
def results(opts={}):
	data = opts['data']
	sequences = opts['sequences']
	
	return render("results.html.jinja2", {
		"data": data,
		"sequences": sequences,
		"input_width": sum(len(s) for s in sequences)
	})

# === alignment ===

# Renders alignment detail page
def alignment(params):
	return render("alignment.html.jinja2", params)

# === render ===

# Render [Jinja2](http://jinja.pocoo.org/docs/) template from directory `epb/templates`
def render(action, context={}):
	return environment_for(action).get_template(action).render(context)

def environment_for(action):
	if action.endswith(".js") or action.endswith(".js.jinja2"):
		return javascript_environment()
	else:
		return html_environment()

def loader():
	return jinja2.PackageLoader('epb', 'templates')

def html_environment():
	env = jinja2.Environment(loader = loader())
	env.filters['as_percent'] = lambda value, total: "{0}%".format(value * 100.0 / total)
	env.filters['map_function'] = lambda enum, name: (eval(name)(e) for e in enum)
	env.filters['verticalize'] = lambda s: "<br/>".join(list(str(s)))
	env.globals['render'] = render
	return env

def javascript_environment():
	env = jinja2.Environment(
		loader = loader(),
		block_start_string = "<%",
		block_end_string = "%>",
		variable_start_string = "<%=",
		variable_end_string = "%>"
	)
	env.globals['render'] = render
	return env
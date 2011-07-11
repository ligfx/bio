# [Back to docs.py](docs.html)

import jinja2

import epb.fasta as Fasta
from epb.blast import Blast

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
def results(params):
	names = params["names"]
	fasta = params["sequence"]
	method = params["method"]
	
	if method == 'concat':
		seq = Fasta.normalize(fasta)
	elif method == 'multiple':
		seq = fasta
	else:
		raise Exception, "method must be one of 'concat' or 'multiple'"
	
	blast = Blast({"database_path": params['dbdir']})
	data = blast.find_all(seq, names)
	
	sequences = list(Fasta.each(fasta))
	
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
	env = jinja2.Environment(loader = jinja2.PackageLoader('epb', 'templates'))
	env.filters['as_percent'] = lambda value, total: "{0}%".format(value * 100.0 / total)
	env.filters['map_function'] = lambda enum, name: (eval(name)(e) for e in enum)
	env.globals['render'] = render
	return env
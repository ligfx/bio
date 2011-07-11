# EukPhyloBlast-Py uses [Pycco](http://fitzgen.github.com/pycco/) to generate documentation.
#
# Running
#
#     pip install pycco
#     pycco epb/*.py
#
# will generate HTML documentation for all source files, saving it into the `docs` folder by default.
#
# ## Files
#
# * [\_\_init__.py](__init__.html): The good stuff.
# * [[blast.py]]: Interface with `blastall`
# * [[controller.py]]: Takes params, does stuff, renders the result
# * [[fasta.py]]: Shim on top of [BioPy's SeqIO](http://www.biopython.org/DIST/docs/api/Bio.SeqIO-module.html)
# * [[presenter.py]]: Massaging results from [BioPy's NCBIXML](http://www.biopython.org/DIST/docs/api/Bio.Blast.Record-module.html) into more palatable forms
# * [[process.py]]: Interface for running processes
# * [[taxon.py]]: Reading organism names from the `Taxon_%s.txt` files
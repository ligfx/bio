import cgi
import os
import time

# === Request ===
#
# Abstracts over a CGI request
class Request:
	# **Properties:** `categories`, `method`, `sequence`
	def __init__(self):
		form = cgi.FieldStorage()
		
		self.missing = []
		
		self.sequence = form.getvalue("sequence", None)
		if not self.sequence: self.missing.append('sequence')
		self.method = form.getvalue("method", None)
		if not self.method: self.missing.append('method')
		self.categories = form.getlist("category")
		if not any(self.categories): self.missing.append('category')

# === Job ===
#
# Abstracts over a EukPhyloBlast job.
class Job:
	def __init__(self, diskpath, httppath):
		self.id = int(time.time())
		
		self.output_directory = os.path.join(diskpath, str(self.id))
		os.makedirs(self.output_directory)
		
		self.alignment_directory = os.path.join(self.output_directory, "alignments")
		os.makedirs(self.alignment_directory)

		self.status_file_path = os.path.join(self.output_directory, "status.html")
		self.results_file_path = os.path.join(self.output_directory, "results.html")
		
		self.output_http_path = os.path.join(httppath, str(self.id))
		self.status_http_path = os.path.join(self.output_http_path, "status.html")
	
	# === alignment_file ===
	def alignment_file(self, key):
		alignment_file_path = os.path.join(self.alignment_directory, "%s.html" % key)
		return open(alignment_file_path, "w")

	# === status_file ===
	def status_file(self):
		return atomicfile(self.status_file_path)

	# === results_file ===
	def results_file(self):
		return open(self.results_file_path, "w")


# === atomicfile ===
#
# Abstracts over writing to a temp file, then atomically renaming
# over an existing file
class atomicfile:
	def __init__(self, path):
		self.temp_path = path + "_temp"
		self.real_path = path

		self.file = open(self.temp_path, "w")

	def __enter__(self):
		return self.file

	def __exit__(self, type, value, traceback):
		self.file.close()
		# `value` is an exception, or None
		if not value:
			os.rename(self.temp_path, self.real_path)
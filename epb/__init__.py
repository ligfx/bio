from os import path
import yaml

class config:
	def __init__(self, directory=path.dirname(__file__)):
		self.directory = directory
		self.configfile = path.join(self.directory, 'config.yaml')
		with open(self.configfile) as f:
			self.config = yaml.load(f)
		self.blast_dir = self.absolute_directory(self.config['blast_dir'])
		self.db_dir = self.absolute_directory(self.config['db_dir'])
		self.info_dir = self.absolute_directory(self.config['info_dir'])
		self.results_output_dir = self.absolute_directory(self.config['results_output_dir'])
		self.results_http_dir = self.config['results_http_dir']
		self.organism_lists_dir = self.absolute_directory(self.config['organism_lists_dir'])
	
	def __getitem__(self, key):
		return self.config[key]
	
	def absolute_directory(self, directory):
		if directory.startswith("/"):
			return directory
		else:
			return path.join(self.directory, directory)
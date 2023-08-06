# coding: utf-8

import logging
import optparse
import os

#---------------------------------------------------------------------------# 
class Config:
	def __init__(self, desc):
		self._parser = optparse.OptionParser(description=desc)
		self._parser.add_option("-v", "--verbosity", action="count", default=0,
			help='increase output verbosity (optional)')
		self._parser.add_option("--dry-run", action="store_true", default=False,
			help='Dry run option (optional)')
		self._parser.add_option("-i", "--input-directory", type=str,
			default="",
			help='input photo directory')
		self._parser.add_option("-o", "--output-directory", type=str,
			default="./output",
			help='output photo directory')
		self._log = logging.getLogger("config")

	def parse(self):
		(options, args) = self._parser.parse_args()

		self._input_directory  = options.input_directory
		self._output_directory = options.output_directory
		
		self._dry_run = options.dry_run
		self._verbosity = options.verbosity

	def check(self) -> bool:
		result = True

		if not os.path.isdir(self._input_directory):
			self._log.error("input directory is invalid ({})".format(self._input_directory))
			result = False

		if not os.path.exists(self._output_directory):
			os.makedirs(self._output_directory, exist_ok=True)
		else:	
			if not os.path.isdir(self._output_directory):
				self._log.error("output directory is invalid ({})".format(self._output_directory))
				result = False

		return result

	def log(self, level = logging.INFO) -> None:
		self._log.log(level, "input directory : {}".format(self._input_directory))
		self._log.log(level, "output directory: {}".format(self._output_directory))
		self._log.log(level, "dry run         : {}".format(self._dry_run))
		self._log.log(level, "verbosity       : {}".format(self._verbosity))

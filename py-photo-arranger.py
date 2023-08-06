#!/usr/bin/env python3

import logging
import sys
import src.arranger
import src.config

# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
	config = src.config.Config("Application to arrange photos based on meta data.")
	config.parse()

	logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%m-%y %H:%M:%S')
	log = logging.getLogger()
	log.setLevel(logging.WARNING)

	if not config.check():
		sys.exit(1)

	# Configure logger
	if int(config._verbosity) > 0:
		if int(config._verbosity) > 1:
			log.setLevel(logging.DEBUG)
		else:
			log.setLevel(logging.INFO)

	config.log()

	arranger = src.arranger.Arranger(config._input_directory, config._output_directory, config._dry_run)
	arranger.process()

	logging.info('Done')

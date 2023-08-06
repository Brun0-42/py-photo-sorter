# coding: utf-8

import logging
import os
import piexif
import time
import shutil

#---------------------------------------------------------------------------# 
class Arranger:
	def __init__(self, input_directory, output_directory, dry_run=False):
		self._input_directory  = input_directory
		self._output_directory = output_directory
		self._dry_run = dry_run

		self._log = logging.getLogger("arranger")

		self._months = {
			"00": "xx_unsorted",
			"01": "01_janvier",
			"02": "02_fevrier",
			"03": "03_mars",
			"04": "04_avril",
			"05": "05_mai",
			"06": "06_juin",
			"07": "07_juillet",
			"08": "08_aout",
			"09": "09_septembre",
			"10": "10_octobre",
			"11": "11_novembre",
			"12": "12_decembre",
		}
		self._files_nb = 0
		self._copied_files_nb = 0
		self._ignored_files_nb = 0
		self._unsupported_files_nb = 0

	def _copy_to_unsupported(self, filename):
		self._log.debug("moving supported file '{}'' to '{}'".format(filename, "Unsupported"))
		self._unsupported_files_nb += 1

		if not self._dry_run:
			dirPath = os.path.join(self._output_directory, "Unsupported")
			os.makedirs(dirPath, exist_ok=True)
			fileOutPath = os.path.join(dirPath, os.path.basename(filename))
			shutil.move(filename, fileOutPath)


	def _move_file(self, filename, year, month):
		self._log.info("moving file '{}'' to '{}/{}'".format(filename, year, self._months[month]))
		self._copied_files_nb += 1

		dirPath = os.path.join(self._output_directory, year)
		dirPath = os.path.join(dirPath, self._months[month])

		os.makedirs(dirPath, exist_ok=True)
		fileOutPath = os.path.join(dirPath, os.path.basename(filename))

		if not self._dry_run:
			shutil.move(filename, fileOutPath)

	def _get_photo_year_month(self, file_path):
		try:
			tags = piexif.load(file_path)
			for tag in tags:
				if "Exif" in tag:
					#self._log.debug('tag: {}'.format(tag))
					for subtag in tags['Exif']:
						#self._log.debug('subtag: {}'.format(subtag))
						if piexif.ExifIFD.DateTimeOriginal == subtag:
							timestamp = tags['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
							self._log.debug("modification time for EXIF file '{}': {}".format(file_path, str(timestamp)))
							tolkens = str(timestamp).split(":")
							year = tolkens[0]
							month = tolkens[1]
							return year, month
		except Exception as e:
			self._log.error("Error reading metadata from  '{}': '{}'".format(file_path, e))

		timestamp = time.strftime("%Y:%m:%d", time.strptime(time.ctime(os.path.getmtime(file_path))))
		self._log.debug('Last modification time for file ({}): {}'.format(file_path, timestamp))
		timestamp = timestamp.split(":")
		year = timestamp[0]
		month = timestamp[1]
		return year, month

	def _process_one_file(self, filename):
		self._log.debug('----------------------------')
		self._log.debug('filename: {}'.format(filename))
		self._files_nb += 1

		extension = os.path.splitext(filename)[1].lower()
		if(extension == ".jpg" or extension ==".jpeg"):
			year, month = self._get_photo_year_month(filename)
			self._move_file(filename, year, month)
		elif (extension == ".tiff"):
			self._log.debug("'tiff' files not supported")
			self._copy_to_unsupported(filename)
		elif (extension == ".mp4"):
			self._log.debug("'mp4' files not supported")
			self._copy_to_unsupported(filename)
		elif (extension == ".png"):
			self._log.debug("'PNG' files not supported")
			self._copy_to_unsupported(filename)
		elif (extension == ".avi"):
			self._log.debug("'avi' files not supported")
			self._copy_to_unsupported(filename)
		elif (extension == ".mov" or extension == ".MOV"):
			self._log.debug("'mov' files not supported")
			self._copy_to_unsupported(filename)
		else:
			self._ignored_files_nb += 1
			self._log.warning("did not recognize file type for '{}' ('{}')".format(filename, extension))
			return;

	def process(self):
		for root, dirs, filenames in os.walk(self._input_directory):
			for filename in filenames:
				self._process_one_file(os.path.join(root, filename))

		self._log.info("Files processed:    {}".format(self._files_nb))
		self._log.debug("Files copied:      {}".format(self._copied_files_nb))
		self._log.debug("Files ignored:     {}".format(self._ignored_files_nb))
		self._log.debug("Files unsupported: {}".format(self._unsupported_files_nb))

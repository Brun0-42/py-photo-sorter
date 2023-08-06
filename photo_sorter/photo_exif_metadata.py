# coding: utf-8

from loguru import logger
from PIL import Image

import loguru_decorator
import piexif
import time
import os
import datetime

#-----------------------------------------------------------------------------# 
def _xp_decode(t):
    """
    Takes a exif XPKeywords tag and decodes it to a text string
    """
    b = bytes(t)
    return b[:-2].decode('utf-16-le')

#-----------------------------------------------------------------------------# 
def _xp_encode(s):
    """
    Takes a text string and encodes it as an exif XPKeywords tag
    """
    b = s.encode('utf-16-le') + b'\x00\x00'
    return tuple([int(i) for i in b])

#-----------------------------------------------------------------------------# 
class PhotoExifMetadata:
    def __init__(self, file_path):
        self._file_path  = file_path

    @loguru_decorator.logger_wraps(level="DEBUG")
    def print(self):
        try:
            image = Image.open(self._file_path)
            exif_dict = piexif.load(image.info["exif"])
            for ifd in ("0th", "Exif"):
                for tag in exif_dict[ifd]:
                    tag_name = piexif.TAGS[ifd][tag]["name"]
                    tag_type = piexif.TAGS[ifd][tag]["type"]
                    tag_value = exif_dict[ifd][tag]

                    if tag_type == piexif.TYPES.Byte:
                        tag_value = _xp_decode(tag_value)
                    elif (tag_type == piexif.TYPES.Ascii):
                        tag_value = tag_value.decode('utf-8')
                    elif (tag_type == piexif.TYPES.Undefined):
                        tag_value = ""
                    if tag_value:
                        print(f"  {tag_name} ({tag_type}): {tag_value}")
        except Exception as e:
            logger.error(f"Error reading EXIF data ({self._file_path}): {e}")

    @loguru_decorator.logger_wraps(level="ERROR")
    def get_xp_title(self):
        """
        Reads the exif XPKeyword tags of an image and returns them as a stirng
        """
        im = Image.open(self._file_path)
        exif_dict = piexif.load(im.info["exif"])
        print(exif_dict["0th"])
        value = exif_dict["0th"][piexif.ImageIFD.XPTitle]
        value = _xp_decode(value)
        im.close()
        return value

    @loguru_decorator.logger_wraps(level="ERROR")
    def get_xp_keywords(self):
        """
        Reads the exif XPKeyword tags of an image and returns them as a stirng
        """
        im = Image.open(self._file_path)
        exif_dict = piexif.load(im.info["exif"])
        print(exif_dict["0th"])
        keyword = exif_dict["0th"][piexif.ImageIFD.XPKeywords]
        keyword = _xp_decode(keyword)
        im.close()
        return keyword

    @loguru_decorator.logger_wraps(level="ERROR")
    def get_xp_comment(self):
        """
        Reads the exif XPKeyword tags of an image and returns them as a stirng
        """
        try:
            im = Image.open(self._file_path)
            exif_dict = piexif.load(im.info["exif"])
            print(exif_dict["0th"])
            keyword = exif_dict["0th"][piexif.ImageIFD.XPComment]
            keyword = _xp_decode(keyword)
            im.close()
            return keyword
        except Exception as e:
            logger.error("no xp comment for {} (except: {})".format(self._file_path, e))
            return None

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_xp_title(self, string):
        """
        Writes exif XPKeyword tags to an image
        """
        im = Image.open(self._file_path)
        keyword = _xp_encode(string)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.XPTitle] = keyword
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_title(self, string):
        """
        Writes exif XPKeyword tags to an image
        """
        im = Image.open(self._file_path)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = string.encode('utf-8')
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_xp_subject(self, string):
        """
        Writes exif XPKeyword tags to an image
        """
        im = Image.open(self._file_path)
        keyword = _xp_encode(string)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.XPSubject] = keyword
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_xp_keywords(self, string):
        """
        Writes exif XPKeyword tags to an image
        """
        im = Image.open(self._file_path)
        keyword = _xp_encode(string)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keyword
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_xp_comment(self, string):
        """
        Writes exif XPKeyword tags to an image
        """
        im = Image.open(self._file_path)
        keyword = _xp_encode(string)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.XPComment] = keyword
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_xp_author(self, string):
        """
        Writes exif XPKeyword tags to an image
        """
        im = Image.open(self._file_path)
        value = _xp_encode(string)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.XPAuthor] = value
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def get_xp_author(self):
        """
        Reads the exif XPAuthor tag of an image and returns it as a string
        """
        im = Image.open(self._file_path)
        exif_dict = piexif.load(im.info["exif"])
        author = exif_dict["0th"][piexif.ImageIFD.XPAuthor]
        author = _xp_decode(author)
        im.close()
        return author
    
    @loguru_decorator.logger_wraps(level="ERROR")
    def write_author(self, author_name):
        im = Image.open(self._file_path)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.Artist] = author_name.encode('utf-8')
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)
    # @loguru_decorator.logger_wraps(level="ERROR")
    # def write_copyright(self, string):
    #     """
    #     Writes exif XPKeyword tags to an image
    #     """
    #     im = Image.open(self._file_path)
    #     value = _xp_encode(string)
    #     exif_dict = piexif.load(im.info["exif"])
    #     exif_dict["0th"][piexif.ImageIFD.Copyright] = value
    #     exif_bytes = piexif.dump(exif_dict)
    #     im.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def get_file_modification_time(self):
        """Retrieve the file modification time."""
        timestamp = os.path.getmtime(self._file_path)
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y:%m:%d %H:%M:%S')

    @loguru_decorator.logger_wraps(level="ERROR")
    def get_datetime_taken(self):
        """Retrieve the date taken from the EXIF data."""
        try:
            tags = piexif.load(self._file_path)
            for tag in tags:
                if "Exif" in tag:
                    for subtag in tags['Exif']:
                        if piexif.ExifIFD.DateTimeOriginal == subtag:
                            timestamp = tags['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
                            logger.error("EXIF self._file_path '{}': {}".format(self._file_path, str(timestamp)))
                            return timestamp
        except Exception as e:
            logger.error("Error reading metadata from  '{}': '{}'".format(self._file_path, e))

    @loguru_decorator.logger_wraps(level="ERROR")
    def set_datetime_taken(self, datetime_taken):
        """
        Sets the date taken in the EXIF data of the image.
        """
        try:
            tags = piexif.load(self._file_path)
            if "Exif" in tags:
                tags["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime_taken.encode()
                exif_bytes = piexif.dump(tags)
                im = Image.open(self._file_path)
                im.save(self._file_path, exif=exif_bytes)
                logger.info("Date taken set successfully.")
            else:
                logger.error("No EXIF data found in the image.")
        except Exception as e:
            logger.error("Error reading metadata from  '{}': '{}'".format(self._file_path, e))

    @loguru_decorator.logger_wraps(level="DEBUG")
    def get_photo_year_month(self):
        try:
            tags = piexif.load(self._file_path)
            for tag in tags:
                if "Exif" in tag:
                    #logger.debug('tag: {}'.format(tag))
                    for subtag in tags['Exif']:
                        #logger.debug('subtag: {}'.format(subtag))
                        if piexif.ExifIFD.DateTimeOriginal == subtag:
                            timestamp = tags['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
                            logger.error("modification time for EXIF self._file_path '{}': {}".format(self._file_path, str(timestamp)))
                            tolkens = str(timestamp).split(":")
                            year = tolkens[0]
                            month = tolkens[1]
                            return year, month
        except Exception as e:
            logger.error("Error reading metadata from  '{}': '{}'".format(self._file_path, e))

        timestamp = time.strftime("%Y:%m:%d", time.strptime(time.ctime(os.path.getmtime(self._file_path))))
        logger.error("Last modification time for '{}': {}".format(self._file_path, timestamp))
        timestamp = timestamp.split(":")
        year = timestamp[0]
        month = timestamp[1]
        return year, month

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_copyright(self, copyright_text):
        # Load the image
        image = Image.open(self._file_path)

        # Get existing EXIF data
        exif_dict = piexif.load(image.info['exif']) if 'exif' in image.info else {}

        # Add or update copyright information
        exif_dict['0th'][piexif.ImageIFD.Copyright] = copyright_text.encode('utf-8')

        # Convert the EXIF data back to bytes
        exif_bytes = piexif.dump(exif_dict)

        # Save the image with the new EXIF data
        image.save(self._file_path, exif=exif_bytes)

    @loguru_decorator.logger_wraps(level="ERROR")
    def write_author(self, author_name):
        im = Image.open(self._file_path)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.Artist] = author_name.encode('utf-8')
        exif_bytes = piexif.dump(exif_dict)
        im.save(self._file_path, exif=exif_bytes)

# if __name__ == "__main__":
#     my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
#     print(f"{my_photo_metadata.get_file_modification_time()=}")

# coding: utf-8

from loguru import logger
from PIL import Image
import piexif
import os
import datetime
import time
import loguru_decorator

#-----------------------------------------------------------------------------# 
def _xp_decode(t):
    """
    Takes an EXIF XPKeywords tag and decodes it to a text string.
    """
    b = bytes(t)
    return b[:-2].decode('utf-16-le')

#-----------------------------------------------------------------------------# 
def _xp_encode(s):
    """
    Takes a text string and encodes it as an EXIF XPKeywords tag.
    """
    b = s.encode('utf-16-le') + b'\x00\x00'
    return tuple([int(i) for i in b])

#-----------------------------------------------------------------------------# 
class PhotoExifMetadata:
    def __init__(self, file_path):
        self._file_path = file_path

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="DEBUG")
    def print(self):
        try:
            with Image.open(self._file_path) as image:
                exif_dict = piexif.load(image.info["exif"])
                for ifd in ("0th", "Exif"):
                    for tag in exif_dict[ifd]:
                        tag_name = piexif.TAGS[ifd][tag]["name"]
                        tag_type = piexif.TAGS[ifd][tag]["type"]
                        tag_value = exif_dict[ifd][tag]

                        if tag_type == piexif.TYPES.Byte:
                            tag_value = _xp_decode(tag_value)
                        elif tag_type == piexif.TYPES.Ascii:
                            tag_value = tag_value.decode('utf-8')
                        elif tag_type == piexif.TYPES.Undefined:
                            tag_value = ""
                        if tag_value:
                            print(f"  {tag_name} ({tag_type}): {tag_value}")
        except Exception as e:
            logger.error(f"Error reading EXIF data ({self._file_path}): {e}")

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def _read_exif_tag(self, exif_key, exif_tag):
        """
        Reads an EXIF tag from an image
        """
        try:
            with Image.open(self._file_path) as im:
                exif_dict = piexif.load(im.info["exif"])
                value = exif_dict[exif_key][exif_tag]
                return value
        except KeyError:
            logger.error(f"No {exif_key}/{exif_tag} tag found in {self._file_path}")
            return None

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def _write_exif_tag(self, exif_key, exif_tag, exif_value):
        """
        Writes the EXIF tag to an image.
        """
        try:
            with Image.open(self._file_path) as image:
                exif_dict = piexif.load(image.info["exif"]) if "exif" in image.info else {}
                print("toto")
                print(f"{exif_dict=}")
                exif_dict[exif_key][exif_tag] = exif_value
                print("toto")
                exif_bytes = piexif.dump(exif_dict)
                print("titi")
                print(f"{exif_bytes=}")
                image.save(self._file_path, exif=exif_bytes)
        except Exception as e:
            tag_name = piexif.TAGS[exif_key][exif_tag]["name"]
            print(f"{tag_name=}")
            print(f"{exif_key=}")

            logger.error(f"Error writing EXIF data ({exif_key}{tag_name}) in {self._file_path}: {e}")

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_xp_author(self):
        """
        Reads the EXIF XPAuthor tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.XPAuthor)
        if exif_value:
            return _xp_decode(exif_value)
        else:
            return None

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_xp_author(self, value):
        """
        Writes the EXIF XPAuthor tag to an image.
        """
        self._write_exif_tag("0th", piexif.ImageIFD.XPAuthor, _xp_encode(value))

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_xp_title(self):
        """
        Reads the EXIF XPTitle tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.XPTitle)
        if exif_value:
            return _xp_decode(exif_value)
        else:
            return None

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_xp_title(self, value):
        """
        Writes the EXIF XPTitle tag to an image.
        """
        exif_value = _xp_encode(value)
        self._write_exif_tag("0th", piexif.ImageIFD.XPTitle, exif_value)

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_xp_keywords(self):
        """
        Reads the EXIF XPKeywords tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.XPKeywords)
        if exif_value:
            return _xp_decode(exif_value)
        else:
            return None

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_xp_keywords(self, value):
        """
        Writes the EXIF XPTitle tag to an image.
        """
        exif_value = _xp_encode(value)
        self._write_exif_tag("0th", piexif.ImageIFD.XPKeywords, exif_value)

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_xp_subject(self):
        """
        Reads the EXIF XPSubject tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.XPSubject)
        if exif_value:
            return _xp_decode(exif_value)
        else:
            return None
        
    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_xp_subject(self, value):
        """
        Writes the EXIF XPSubject tag to an image.
        """
        exif_value = _xp_encode(value)
        self._write_exif_tag("0th", piexif.ImageIFD.XPSubject, exif_value)

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_xp_comment(self):
        """
        Reads the EXIF XPComment tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.XPComment)
        if exif_value:
            return _xp_decode(exif_value)
        else:
            return None

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_xp_comment(self, value):
        """
        Writes the EXIF XPComment tag to an image.
        """
        exif_value = _xp_encode(value)
        self._write_exif_tag("0th", piexif.ImageIFD.XPComment, exif_value)

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_title(self):
        """
        Reads the EXIF ImageDescription tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.ImageDescription)
        if exif_value:
            return exif_value.decode('utf-8')
        else:
            return None
        
    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_title(self, value):
        """
        Writes the EXIF ImageDescription tag to an image.
        """
        exif_value = value.encode('utf-8')
        self._write_exif_tag("0th", piexif.ImageIFD.ImageDescription, exif_value)

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_artist(self):
        """
        Reads the EXIF Artist tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.Artist)
        if exif_value:
            return exif_value.decode('utf-8')
        else:
            return None
        
    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_artist(self, value):
        """
        Writes the EXIF Artist tag to an image.
        """
        exif_value = value.encode('utf-8')
        self._write_exif_tag("0th", piexif.ImageIFD.Artist, exif_value)

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_copyright(self):
        """
        Reads the EXIF Copyright tag of an image and returns it as a string.
        """
        exif_value = self._read_exif_tag("0th", piexif.ImageIFD.Copyright)
        if exif_value:
            return exif_value.decode('utf-8')
        else:
            return None
        
    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_copyright(self, value):
        """
        Writes the EXIF Copyright tag to an image.
        """
        exif_value = value.encode('utf-8')
        self._write_exif_tag("0th", piexif.ImageIFD.Copyright, exif_value)

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_file_modification_time(self):
        """
        Retrieve the file modification time.
        """
        timestamp = os.path.getmtime(self._file_path)
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y:%m:%d %H:%M:%S')

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def get_datetime_taken(self):
        """
        Retrieve the date taken from the EXIF data.
        """
        exif_value = self._read_exif_tag("Exif", piexif.ExifIFD.DateTimeOriginal)
        if exif_value:
            return exif_value.decode()
        else:
            return None

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="ERROR")
    def set_datetime_taken(self, value):
        """
        Sets the date taken in the EXIF data of the image.
        """
        self._write_exif_tag("Exif", piexif.ExifIFD.DateTimeOriginal, value.encode())

    @loguru_decorator.logger_wraps(level="DEBUG")
    @logger.catch(level="DEBUG")
    def get_photo_year_month(self):
        """
        Retrieve the year and month the photo was taken from the EXIF data.
        """
        try:
            timestamp = self.get_datetime_taken()
            if timestamp:
                timestamp = timestamp.decode()
                year, month, _ = timestamp.split(":")
                return year, month
        except Exception as e:
            logger.error(f"Error reading metadata from '{self._file_path}': {e}")

        timestamp = time.strftime("%Y:%m:%d", time.strptime(time.ctime(os.path.getmtime(self._file_path))))
        logger.error(f"Last modification time for '{self._file_path}': {timestamp}")
        year, month, _ = timestamp.split(":")
        return year, month

import pytest
import datetime
import os

from photo_exif_metadata import PhotoExifMetadata

def test_file_path():
    my_photo_metadata = PhotoExifMetadata("toto")
    assert my_photo_metadata._file_path == "toto"

def test_file_path():
    my_photo_metadata = PhotoExifMetadata("toto")
    assert my_photo_metadata._file_path == "toto"

def test_get_file_modification_time():
    file_path = "./res/python-logo.jpg"
    timestamp = os.path.getmtime(file_path)
    datetime_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y:%m:%d %H:%M:%S')

    my_photo_metadata = PhotoExifMetadata(file_path)
    assert my_photo_metadata.get_file_modification_time() == datetime_str
    my_photo_metadata.set_datetime_taken(datetime_str)
    assert my_photo_metadata.get_datetime_taken() == datetime_str

    tolkens = str(datetime_str).split(":")
    photo_tolkens = my_photo_metadata.get_photo_year_month()
    assert photo_tolkens[0] == tolkens[0]
    assert photo_tolkens[1] == tolkens[1]

# def test_get_datetime_taken():
#     my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
#     assert my_photo_metadata.get_datetime_taken() == "2024:08:30 17:56:32"

# def test_get_photo_year_month():
#     my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
#     assert my_photo_metadata.get_photo_year_month() == "2024"

def test_write_author():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.write_xp_author("John Doe")
    assert my_photo_metadata.get_xp_author() == "John Doe"
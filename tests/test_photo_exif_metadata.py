import pytest
import datetime
import os

from photo_exif_metadata import PhotoExifMetadata

def test_file_path():
    my_photo_metadata = PhotoExifMetadata("toto")
    assert my_photo_metadata._file_path == "toto"

def test_get_file_modification_time():
    file_path = "./res/python-logo.jpg"
    timestamp = os.path.getmtime(file_path)
    datetime_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y:%m:%d %H:%M:%S')

    my_photo_metadata = PhotoExifMetadata(file_path)
    print(f"{datetime_str=}")
    my_photo_metadata.set_datetime_taken(datetime_str)
    print(my_photo_metadata.get_datetime_taken())
    assert my_photo_metadata.get_datetime_taken() == datetime_str

    tolkens = str(datetime_str).split(":")
    photo_tolkens = my_photo_metadata.get_photo_year_month()
    assert photo_tolkens[0] == tolkens[0]
    assert photo_tolkens[1] == tolkens[1]

def test_write_read_xp_author():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_xp_author("John Doe")
    assert my_photo_metadata.get_xp_author() == "John Doe"

def test_write_read_xp_title():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_xp_title("Python Logo")
    assert my_photo_metadata.get_xp_title() == "Python Logo"

def test_write_read_xp_keywords():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_xp_keywords("#titi, #toto")
    assert my_photo_metadata.get_xp_keywords() == "#titi, #toto"

def test_write_read_xp_subject():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_xp_subject("xp_subject")
    assert my_photo_metadata.get_xp_subject() == "xp_subject"

def test_write_read_xp_comment():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_xp_comment("xp_comment")
    assert my_photo_metadata.get_xp_comment() == "xp_comment"

def test_write_read_title():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_title("title")
    assert my_photo_metadata.get_title() == "title"

def test_write_read_artist():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_artist("artist")
    assert my_photo_metadata.get_artist() == "artist"

def test_write_read_copyright():
    my_photo_metadata = PhotoExifMetadata("./res/python-logo.jpg")
    my_photo_metadata.set_copyright("copyright")
    assert my_photo_metadata.get_copyright() == "copyright"

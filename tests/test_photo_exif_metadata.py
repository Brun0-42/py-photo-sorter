import pytest
import datetime
import os
import shutil

from photo_exif_metadata import PhotoExifMetadata

def test_file_path():
    my_photo_metadata = PhotoExifMetadata("toto")
    assert my_photo_metadata._file_path == "toto"

@pytest.fixture
def test_config() -> str:
    _file_path = "./res/test.jpg"

    # Setting up resources...
    shutil.copy2("./res/python-logo.jpg", _file_path)

    yield _file_path

    # Clean up resources (if any) after the test
    os.remove(_file_path)

def test_read_write(test_config) -> None:
    file_path = test_config

    my_photo_writer = PhotoExifMetadata(file_path)
    assert my_photo_writer.get_copyright() == None
    assert my_photo_writer.get_artist() == None
    assert my_photo_writer.get_title() == None
    assert my_photo_writer.get_xp_comment() == None
    assert my_photo_writer.get_xp_subject() == None

    my_photo_writer.set_copyright("copyright")
    my_photo_writer.set_artist("artist")
    my_photo_writer.set_title("title")
    my_photo_writer.set_xp_comment("xp_comment")
    my_photo_writer.set_xp_subject("xp_subject")
    my_photo_writer.__del__()

    my_photo_reader = PhotoExifMetadata(file_path)
    assert my_photo_reader.get_copyright() == "copyright"
    assert my_photo_reader.get_artist() == "artist"
    assert my_photo_reader.get_title() == "title"
    assert my_photo_reader.get_xp_comment() == "xp_comment"
    assert my_photo_reader.get_xp_subject() == "xp_subject"

def test_read_write_no_change(test_config) -> None:
    file_path = test_config

    my_photo_writer = PhotoExifMetadata(file_path, auto_save=False)
    assert my_photo_writer.get_copyright() == None
    assert my_photo_writer.get_artist() == None
    assert my_photo_writer.get_title() == None
    assert my_photo_writer.get_xp_comment() == None
    assert my_photo_writer.get_xp_subject() == None

    my_photo_writer.set_copyright("copyright")
    my_photo_writer.set_artist("artist")
    my_photo_writer.set_title("title")
    my_photo_writer.set_xp_comment("xp_comment")
    my_photo_writer.set_xp_subject("xp_subject")
    my_photo_writer.__del__()

    my_photo_reader = PhotoExifMetadata(file_path)
    my_photo_reader.load()
    assert my_photo_reader.get_copyright() == None
    assert my_photo_reader.get_artist() == None
    assert my_photo_reader.get_title() == None
    assert my_photo_reader.get_xp_comment() == None
    assert my_photo_reader.get_xp_subject() == None

def test_get_file_modification_time(test_config) -> None:
    file_path = test_config

    timestamp = os.path.getmtime(file_path)
    datetime_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y:%m:%d %H:%M:%S')

    my_photo_writer = PhotoExifMetadata(file_path)
    my_photo_reader = PhotoExifMetadata(file_path)
    
    my_photo_writer.load()
    my_photo_writer.set_datetime_taken(datetime_str)
    my_photo_writer.save()

    my_photo_reader.load()
    assert my_photo_reader.get_datetime_taken() == datetime_str

    tolkens = str(datetime_str).split(":")
    photo_tolkens = my_photo_reader.get_photo_year_month()
    assert photo_tolkens[0] == tolkens[0]
    assert photo_tolkens[1] == tolkens[1]

def test_write_read_xp_author(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_xp_author("John Doe")
    assert my_photo_metadata.get_xp_author() == "John Doe"

def test_write_read_xp_title(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_xp_title("Python Logo")
    assert my_photo_metadata.get_xp_title() == "Python Logo"

def test_write_read_xp_keywords(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_xp_keywords("#titi, #toto")
    assert my_photo_metadata.get_xp_keywords() == "#titi, #toto"

def test_write_read_xp_subject(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_xp_subject("xp_subject")
    assert my_photo_metadata.get_xp_subject() == "xp_subject"

def test_write_read_xp_comment(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_xp_comment("xp_comment")
    assert my_photo_metadata.get_xp_comment() == "xp_comment"

def test_write_read_title(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_title("title")
    assert my_photo_metadata.get_title() == "title"

def test_write_read_artist(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_artist("artist")
    assert my_photo_metadata.get_artist() == "artist"

def test_write_read_copyright(test_config) -> None:
    file_path = test_config

    my_photo_metadata = PhotoExifMetadata(file_path)
    my_photo_metadata.set_copyright("copyright")
    assert my_photo_metadata.get_copyright() == "copyright"

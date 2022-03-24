import pytest
import os
import tempfile

from page_loader import download

DIR_PATH = os.path.dirname(__file__)
SOURCE_PATH = 'https://ru.hexlet.io/courses'
FIXTURE_NAME = 'ru-hexlet-io-courses.html'


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    return open(get_fixture_path(filename)).read()


EXPECTED_DATA = read_file(FIXTURE_NAME)


def test_download(requests_mock):
    requests_mock.get(SOURCE_PATH, text=EXPECTED_DATA)

    with tempfile.TemporaryDirectory() as tmpdirname:
        expected = os.path.join(tmpdirname, FIXTURE_NAME)
        actual = download(SOURCE_PATH, tmpdirname)

        assert EXPECTED_DATA == open(actual).read()
        assert expected == actual

import os
import tempfile
import requests_mock as req_mock

from page_loader import download

DIR_PATH = os.path.dirname(__file__)
SOURCE_PATH = 'https://ru.hexlet.io/courses'

fixture_names = {
    'html_after': 'ru-hexlet-io-courses.html',
    'html_before': 'courses.html',
    'image': 'ru-hexlet-io-assets-professions-python.png',
    'css': 'ru-hexlet-io-assets-application.css',
    'js': 'ru-hexlet-io-packs-js-runtime.js',
    'folder': 'ru-hexlet-io-courses_files',
}


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename):
    return open(get_fixture_path(filename)).read()


before = read_file('before.html')

expected_html = read_file('after.html')
expected_structure = [
    fixture_names['folder'],
    fixture_names['image'],
    fixture_names['js'],
    fixture_names['css'],
    fixture_names['html_after'],
    fixture_names['html_after'],
]


def build_dir_tree(dir_path):
    tree = []

    for _, dirs, files in os.walk(dir_path):
        tree.extend(dirs + files)

    return tree


def test_download(requests_mock):
    requests_mock.get(req_mock.ANY, text=before)

    with tempfile.TemporaryDirectory() as tmpdirname:
        expected = os.path.join(tmpdirname, fixture_names['html_after'])
        actual = download(SOURCE_PATH, tmpdirname)

        assert expected == actual


def test_html_data(requests_mock):
    requests_mock.get(req_mock.ANY, text=before)

    with tempfile.TemporaryDirectory() as tmpdirname:
        actual_html = download(SOURCE_PATH, tmpdirname)

        assert expected_html == read_file(actual_html)


def test_dst_structire(requests_mock):
    requests_mock.get(req_mock.ANY, text=before)

    with tempfile.TemporaryDirectory() as tmpdirname:
        download(SOURCE_PATH, tmpdirname)

        actual_structure = build_dir_tree(tmpdirname)

        assert sorted(expected_structure) == sorted(actual_structure)

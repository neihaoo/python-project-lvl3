import os
import tempfile

from page_loader import download

DIR_PATH = os.path.dirname(__file__)
SOURCE_PATH = 'https://ru.hexlet.io/courses'
ASSERTS_PATH = 'https://ru.hexlet.io/assets/professions/python.png'
FIXTURE_NAME = {
    'html_after': 'ru-hexlet-io-courses.html',
    'html_before': 'courses.html',
    'image': 'ru-hexlet-io-assets-professions-python.png',
    'folder': 'ru-hexlet-io-courses_files',
}


def get_fixture_path(filename, subpath=''):
    return os.path.join(DIR_PATH, 'fixtures', subpath, filename)


def read_file(filename, subpath='', mode='r'):
    return open(get_fixture_path(filename, subpath), mode).read()


before = read_file(FIXTURE_NAME['html_before'], 'before')
after = read_file(FIXTURE_NAME['html_after'], 'after')
image = read_file(
    FIXTURE_NAME['image'],
    os.path.join('after', FIXTURE_NAME['folder']),
    'rb',
)


def check_entry(entry):
    return entry.name if entry.is_file() else [entry.name, list_dir(entry)]


def list_dir(dir_path):
    with os.scandir(dir_path) as it:
        return [check_entry(entry) for entry in it]


def test_download(requests_mock):
    requests_mock.get(SOURCE_PATH, text=before)
    requests_mock.get(
        'https://ru.hexlet.io/assets/professions/python.png',
        content=image,
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        expected = os.path.join(tmpdirname, FIXTURE_NAME['html_after'])
        actual = download(SOURCE_PATH, tmpdirname)

        assert expected == actual


def test_download_html_data(requests_mock):
    requests_mock.get(SOURCE_PATH, text=before)
    requests_mock.get(
        'https://ru.hexlet.io/assets/professions/python.png',
        content=image,
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        actual = download(SOURCE_PATH, tmpdirname)

        assert read_file(actual) == after


def test_download_structire(requests_mock):
    requests_mock.get(SOURCE_PATH, text=before)
    requests_mock.get(
        'https://ru.hexlet.io/assets/professions/python.png',
        content=image,
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        download(SOURCE_PATH, tmpdirname)

        actual = list_dir(tmpdirname)
        expected = list_dir(os.path.join(DIR_PATH, 'fixtures/after'))

        assert expected == actual

import os
import pytest

from page_loader import download
from requests.exceptions import RequestException

DIR_PATH = os.path.dirname(__file__)
ASSETS_FOLDER = 'ru-hexlet-io-courses_files'

urls = {
    'html': 'https://ru.hexlet.io/courses',
    'image': 'https://ru.hexlet.io/assets/professions/python.png',
    'js': 'https://ru.hexlet.io/packs/js/runtime.js',
    'css': 'https://ru.hexlet.io/assets/application.css',
}

names = {
    'html': 'ru-hexlet-io-courses.html',
    'image': 'ru-hexlet-io-assets-professions-python.png',
    'js': 'ru-hexlet-io-packs-js-runtime.js',
    'css': 'ru-hexlet-io-assets-application.css',
}

status_codes = [404, 500]


def get_fixture_path(filename):
    return os.path.join(DIR_PATH, 'fixtures', filename)


def read_file(filename, mode='r'):
    return open(get_fixture_path(filename), mode).read()


contents = {
    'html': read_file('before.html', 'rb'),
    'image': read_file('python.png', 'rb'),
    'js': read_file('runtime.js', 'rb'),
    'css': read_file('application.css', 'rb'),
}


def test_download(requests_mock, tmp_path):
    requests_mock.get(urls['html'], text='data')

    expected = os.path.join(tmp_path, names['html'])
    actual = download(urls['html'], tmp_path)

    assert expected == actual


def test_content(requests_mock, tmp_path):
    requests_mock.get(urls['html'], content=contents['html'])
    requests_mock.get(urls['image'], content=contents['image'])
    requests_mock.get(urls['js'], content=contents['js'])
    requests_mock.get(urls['css'], content=contents['css'])

    html = download(urls['html'], tmp_path)
    image = os.path.join(tmp_path, ASSETS_FOLDER, names['image'])
    js = os.path.join(tmp_path, ASSETS_FOLDER, names['js'])
    css = os.path.join(tmp_path, ASSETS_FOLDER, names['css'])

    assert read_file('after.html') == read_file(html)
    assert contents['image'] == read_file(image, 'rb')
    assert contents['js'] == read_file(js, 'rb')
    assert contents['css'] == read_file(css, 'rb')


def test_os_error(requests_mock):
    with pytest.raises(OSError):
        requests_mock.get(urls['html'], text='data')

        download(urls['html'], 'tmp_path')


@pytest.mark.parametrize('code', status_codes)
def test_request_error(requests_mock, tmp_path, code):
    with pytest.raises(RequestException):
        requests_mock.get(urls['html'], status_code=code)

        download(urls['html'], tmp_path)

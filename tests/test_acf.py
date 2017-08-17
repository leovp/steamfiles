import io
import os
import pytest
from collections import OrderedDict
from steamfiles import acf
from . import sort_dict

test_file_name = os.path.join(os.path.dirname(__file__), 'test_data/appmanifest_202970.acf')


@pytest.fixture(name='acf_data')
def _acf_data():
    with open(test_file_name, 'rt') as f:
        yield f.read()


def test_acf_keys_exist(acf_data):
    data = acf.loads(acf_data)
    assert 'BytesDownloaded' in data['AppState']['DlcDownloads']['202988']
    assert 'BytesToDownload' in data['AppState']['DlcDownloads']['202988']


def test_loads_dumps(acf_data):
    loaded = acf.loads(acf_data)
    assert acf.dumps(sort_dict(loaded)) == acf_data


def test_loads_dumps_with_wrapper(acf_data):
    loaded = acf.loads(acf_data, wrapper=OrderedDict)
    assert isinstance(loaded, OrderedDict)
    assert acf.dumps(loaded) == acf_data


def test_load_dump(acf_data):
    with open(test_file_name, 'rt') as in_file:
        out_file = io.StringIO()
        loaded = acf.load(in_file)
        acf.dump(sort_dict(loaded), out_file)

    # Rewind to the beginning
    out_file.seek(0)
    assert out_file.read() == acf_data


def test_load_dump_with_wrapper(acf_data):
    with open(test_file_name, 'rt') as in_file:
        out_file = io.StringIO()
        loaded = acf.load(in_file, wrapper=OrderedDict)
        acf.dump(loaded, out_file)

    # Rewind to the beginning
    out_file.seek(0)

    assert isinstance(loaded, OrderedDict)
    assert out_file.read() == acf_data


def test_loads_wrong_type():
    with pytest.raises(TypeError):
        acf.loads(b'\x00\x01\x02')


def test_dumps_wrong_type():
    with pytest.raises(TypeError):
        acf.dumps([1, 2, 3])

import io
import os
import pytest
from collections import OrderedDict
from steamfiles import appinfo
from . import sort_dict

test_file_name = os.path.join(os.path.dirname(__file__), 'test_data/appinfo.vdf')


@pytest.yield_fixture
def vdf_data():
    with open(test_file_name, 'rb') as f:
        yield f.read()


@pytest.mark.usefixtures('vdf_data')
def test_loads_dumps(vdf_data):
    loaded = appinfo.loads(vdf_data)
    assert appinfo.dumps(sort_dict(loaded)) == vdf_data


@pytest.mark.usefixtures('vdf_data')
def test_loads_dumps_with_wrapper(vdf_data):
    loaded = appinfo.loads(vdf_data, wrapper=OrderedDict)
    assert isinstance(loaded, OrderedDict)
    assert appinfo.dumps(loaded) == vdf_data


@pytest.mark.usefixtures('vdf_data')
def test_load_dump(vdf_data):
    with open(test_file_name, 'rb') as in_file:
        out_file = io.BytesIO()
        loaded = appinfo.load(in_file)
        appinfo.dump(sort_dict(loaded), out_file)

    # Rewind to the beginning
    out_file.seek(0)
    assert out_file.read() == vdf_data


@pytest.mark.usefixtures('vdf_data')
def test_load_dump_with_wrapper(vdf_data):
    with open(test_file_name, 'rb') as in_file:
        out_file = io.BytesIO()
        loaded = appinfo.load(in_file, wrapper=OrderedDict)
        appinfo.dump(loaded, out_file)

    # Rewind to the beginning
    out_file.seek(0)

    assert isinstance(loaded, OrderedDict)
    assert out_file.read() == vdf_data


def test_loads_wrong_type():
    with pytest.raises(TypeError):
        appinfo.loads('JustTestData')


def test_dumps_wrong_type():
    with pytest.raises(TypeError):
        appinfo.dumps([1, 2, 3])

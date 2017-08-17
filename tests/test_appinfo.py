import io
import os
import pytest
from collections import OrderedDict
from steamfiles import appinfo
from . import sort_dict

test_file_name = os.path.join(os.path.dirname(__file__), 'test_data/appinfo.vdf')


@pytest.fixture(name='vdf_data')
def _vdf_data():
    with open(test_file_name, 'rb') as f:
        yield f.read()


def test_loads_dumps(vdf_data):
    loaded = appinfo.loads(vdf_data)

    # Remove internal helpers, so that they don't interfere with sorting.
    version, universe = loaded.pop(b'__vdf_version'), loaded.pop(b'__vdf_universe')
    sorted_data = sort_dict(loaded)

    # Put internal helpers back in to ensure correct encoding.
    sorted_data.update({b'__vdf_version': version, b'__vdf_universe': universe})

    assert appinfo.dumps(sorted_data) == vdf_data


def test_loads_dumps_with_wrapper(vdf_data):
    loaded = appinfo.loads(vdf_data, wrapper=OrderedDict)
    assert isinstance(loaded, OrderedDict)
    assert appinfo.dumps(loaded) == vdf_data


def test_load_dump(vdf_data):
    with open(test_file_name, 'rb') as in_file:
        out_file = io.BytesIO()
        loaded = appinfo.load(in_file)

        # Remove internal helpers, so that they don't interfere with sorting.
        version, universe = loaded.pop(b'__vdf_version'), loaded.pop(b'__vdf_universe')
        sorted_data = sort_dict(loaded)

        # Put internal helpers back in to ensure correct encoding.
        sorted_data.update({b'__vdf_version': version, b'__vdf_universe': universe})

        appinfo.dump(sorted_data, out_file)

    # Rewind to the beginning
    out_file.seek(0)
    assert out_file.read() == vdf_data


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

import io
import os
import pickle
import pytest
from steamfiles import appinfo

test_file_name = os.path.join(os.path.dirname(__file__), 'test_data/appinfo.vdf')
reference_file_name = os.path.join(os.path.dirname(__file__), 'test_data/appinfo_pickled.bin')


@pytest.yield_fixture
def vdf_data():
    with open(test_file_name, 'rb') as f:
        yield f.read()


@pytest.yield_fixture
def pickled_data():
    with open(reference_file_name, 'rb') as f:
        yield f.read()


@pytest.mark.usefixtures('vdf_data', 'pickled_data')
def test_loads(vdf_data, pickled_data):
    out_file = io.BytesIO()
    parsed = appinfo.loads(vdf_data)
    pickle.dump(parsed, out_file, protocol=3)

    # Rewind to the beginning
    out_file.seek(0)
    assert out_file.read() == pickled_data


def test_loads_wrong_type():
    with pytest.raises(TypeError):
        appinfo.loads('JustTestData')

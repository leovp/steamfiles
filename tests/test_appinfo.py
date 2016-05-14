import io
import os
import pytest
from steamfiles import appinfo

test_file_name = os.path.join(os.path.dirname(__file__), 'test_data/appinfo.vdf')


@pytest.yield_fixture
def vdf_data():
    with open(test_file_name, 'rb') as f:
        yield f.read()


@pytest.mark.usefixtures('vdf_data')
def test_loads_dumps(vdf_data):
    assert appinfo.dumps(appinfo.loads(vdf_data)) == vdf_data


@pytest.mark.usefixtures('vdf_data')
def test_load_dump(vdf_data):
    with open(test_file_name, 'rb') as in_file:
        out_file = io.BytesIO()
        obj = appinfo.load(in_file)
        appinfo.dump(obj, out_file)

    # Rewind to the beginning
    out_file.seek(0)
    assert out_file.read() == vdf_data


def test_loads_wrong_type():
    with pytest.raises(TypeError):
        appinfo.loads('JustTestData')


def test_dumps_wrong_type():
    with pytest.raises(TypeError):
        appinfo.dumps([1, 2, 3])

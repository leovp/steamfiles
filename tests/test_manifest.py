import io
import os
import pytest
from steamfiles import manifest

test_file_name = os.path.join(os.path.dirname(__file__), 'test_data/731.manifest')


@pytest.yield_fixture
def manifest_data():
    with open(test_file_name, 'rb') as f:
        yield f.read()


@pytest.mark.usefixtures('manifest_data')
def test_loads_dumps(manifest_data):
    assert manifest.dumps(manifest.loads(manifest_data)) == manifest_data


@pytest.mark.usefixtures('manifest_data')
def test_load_dump(manifest_data):
    with open(test_file_name, 'rb') as in_file:
        out_file = io.BytesIO()
        obj = manifest.load(in_file)
        manifest.dump(obj, out_file)

    # Rewind to the beginning
    out_file.seek(0)
    assert out_file.read() == manifest_data


def test_loads_wrong_type():
    with pytest.raises(TypeError):
        manifest.loads('JustTestData')


def test_dumps_wrong_type():
    with pytest.raises(TypeError):
        manifest.dumps([1, 2, 3])

import io
import os
import pytest
from steamfiles import acf

test_file_name = os.path.join(os.path.dirname(__file__), 'test_data/appmanifest_202970.acf')


@pytest.yield_fixture
def acf_data():
    with open(test_file_name, 'rt') as f:
        yield f.read()


@pytest.mark.usefixtures('acf_data')
def test_loads_dumps(acf_data):
    assert acf.dumps(acf.loads(acf_data)) == acf_data


@pytest.mark.usefixtures('acf_data')
def test_load_dump(acf_data):
    with open(test_file_name, 'rt') as in_file:
        out_file = io.StringIO()
        obj = acf.load(in_file)
        acf.dump(out_file, obj)

    # Rewind to the beginning
    out_file.seek(0)
    assert out_file.read() == acf_data


def test_loads_wrong_type():
    with pytest.raises(TypeError):
        acf.loads(b'\x00\x01\x02')


def test_dumps_wrong_type():
    with pytest.raises(TypeError):
        acf.dumps([1, 2, 3])

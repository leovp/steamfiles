import pytest
from steamfiles import acf


@pytest.yield_fixture
def acf_data():
    with open('tests/test_data/appmanifest_202970.acf', 'rt') as f:
        yield f.read()


@pytest.mark.usefixtures('acf_data')
def test_loads_dumps(acf_data):
    assert acf.dumps(acf.loads(acf_data)) == acf_data

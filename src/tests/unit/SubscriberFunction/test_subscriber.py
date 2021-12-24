import pytest


@pytest.fixture(scope="function")
def setup():
    print('subscriber setup done.')


def test_sample(setup):
    assert 1 == 1

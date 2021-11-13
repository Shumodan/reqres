import pytest

from core.backend import Backend


@pytest.fixture(scope='session')
def api() -> Backend:
    return Backend()

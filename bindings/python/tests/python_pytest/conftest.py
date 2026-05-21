import pytest


@pytest.fixture(scope="module")
def server():
    """Start server once per test module, tear down after all tests in that module."""
    # TODO: init PMIxServer, register nspace/client
    yield None
    # TODO: finalize server


@pytest.fixture(scope="function")
def client(server):
    """Fresh client for each test, backed by the module-scoped server."""
    # TODO: init PMIxClient with setup_fork env injected
    yield None
    # TODO: finalize client

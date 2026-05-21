import pytest

# Module scope - once per file
@pytest.fixture(scope="module")
def server():
    """ Configure PMIx Server """
    print("Initializing PMIxServer...")
    yield None
    print("Finalizing PMIxServer...")

# Function scope - once per test function
@pytest.fixture(scope="function")
def client(server):
    """ Configure PMIx Client """
    print("Initializing PMIxClient...")
    yield None
    print("Finalizing PMIxClient...")

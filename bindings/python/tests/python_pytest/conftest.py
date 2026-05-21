"""
Pytest fixtures for PMIx python bindings tests.
"""

from server_upcalls import *
import pytest

# Server - module scope - once per file
@pytest.fixture(scope="module")
def server():
    """ Configure PMIx Server """
    print("Initializing PMIxServer...")
    try:
        server = PMIxServer()
    except Exception as e:
        raise RuntimeError(f"FAILED TO CREATE SERVER: {e}")

    server_init_args = [
        {'key':'FOOBAR', 'value':'VAR', 'val_type':PMIX_STRING},
        {'key':'BLAST', 'value':7, 'val_type':PMIX_INT32},
        {'key': 'pmix.tcp.ipv4', 'value': 3333, 'val_type': PMIX_INT},
        {'key': 'pmix.tcp.disipv6', 'value': True,  'val_type': PMIX_BOOL},
        {'key': 'pmix.tcp.repuri',  'value': '-',   'val_type': PMIX_STRING},
    ]

    server_callbacks = {
        'clientconnected': clientconnected,
        'clientfinalized': clientfinalized,
        'fencenb': clientfence,
        'publish': clientpublish,
        'unpublish': clientunpublish,
        'lookup': clientlookup,
        'query': clientquery,
        'registerevents': client_register_events
    }
    
    _ = server.init(server_init_args, server_callbacks)
    is_initialized = server.initialized()

    assert is_initialized, "PMIx Server failed to initialize"
    print("PMIxServer initialized.")

    yield server
    print("Finalizing PMIxServer...")
    del server

# Function scope - once per test function
@pytest.fixture(scope="function")
def client(server):
    """ Configure PMIx Client """
    print(f"Initializing PMIxClient... {server}")
    yield None
    print("Finalizing PMIxClient...")

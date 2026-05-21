"""
Pytest fixtures for PMIx python bindings tests.
"""

from datetime import datetime
import os

from server_upcalls import *
import pytest

# Server - module scope - once per file
@pytest.fixture(scope="module")
def server():
    """ Configure PMIx Server """
    print("Server: Initializing PMIxServer...")
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
    print("Server: PMIxServer initialized.")

    yield server
    print("Finalizing PMIxServer...")
    del server

# Also module scope - initializes once and runs sequential chain of tests
# simple_clients = world of size 1
@pytest.fixture(scope="module")
def simple_client(server):
    """ Configure PMIx Client """
    # Generate randon ns name from date - 2026_06_11_15_30_45_123456
    namespace_name = f"namespace_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}"

    # Register namespace
    (rc, regex) = server.generate_regex(["test000","test001","test002"])
    print("Client: Node regex, rc: ", regex, rc)
    (rc, ppn) = server.generate_ppn(["0,1,2", "3,4,5", "6,7"])
    print("Client: PPN, rc: ", ppn, rc)
    kvals = [{'key':PMIX_NODE_MAP, 'value':regex, 'val_type':PMIX_STRING},
             {'key':PMIX_PROC_MAP, 'value':ppn, 'val_type':PMIX_STRING},
             {'key':PMIX_UNIV_SIZE, 'value':1, 'val_type':PMIX_UINT32},
             {'key':PMIX_JOB_SIZE, 'value':1, 'val_type':PMIX_UINT32}]
    print(f"Client: Registering namespace {namespace_name}...")
    rc = server.register_nspace(namespace_name, 1, kvals)
    print(f"Client: Register namespace return code: {server.error_string(rc)}")

    # register a client
    env = os.environ.copy()    
    uid = os.getuid()
    gid = os.getgid()

    rc = server.register_client({'nspace':namespace_name, 'rank':0}, uid, gid)
    print(f"Client: Register client return code: {server.error_string(rc)}")

    # setup the fork
    rc = server.setup_fork({'nspace':namespace_name, 'rank':0}, env)
    print(f"Client: Setup fork return code: {server.error_string(rc)}")

    yield None
    print("Finalizing PMIxClient...")

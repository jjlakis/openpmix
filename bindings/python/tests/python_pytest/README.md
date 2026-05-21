# OpenPMIx Python Pytest Tests

## Requirements

```
pip install -r requirements.txt
```

The `pmix` Python module must be importable (built and installed from the OpenPMIx tree).

## Run all tests

```
pytest -sv
```

## Run a specific test file

```
pytest test_client_kv.py
```

## Run a specific test

```
pytest test_client_kv.py::TestClientKV::test_put
```

## Fixture scopes

- `server` — started once per test module, shared across all tests in that file
- `client` — created fresh for each individual test

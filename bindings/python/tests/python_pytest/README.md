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
pytest -sv test_client_kv.py
```

## Run a specific test

```
pytest -sv test_client_kv.py::TestClientKV::test_put
```

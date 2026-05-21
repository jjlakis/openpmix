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

## Run locally in Docker

From this directory:

```
# Build image once:
docker build . -t test

# Then, for testing, just mount the working directory in the proper place
docker run --rm --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -e PMIX_MCA_gds=hash -e PMIX_MCA_psec=none -it --name server -v $(pwd):/test --workdir /test test bash
```

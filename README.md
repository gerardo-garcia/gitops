# gitops

This program illustrates a workflow for gitops operations with a Kubernetes cluster. It includes a simple sequence of operations to be tested.

For each operation:

- The repo is cloned and a new branch is created for the operation
- Manifests are prepared according to the requested operation (create cluster, update cluster, delete cluster)
- A commit is generated in the operation branch
- The operation branch is merged onto the main branch
- The main branch is pushed to the remote

## Getting started

```bash
./gitops.py  -h
usage: gitops.py [-h] [-r REPO] [-v]

options:
  -h, --help            show this help message and exit
  -r REPO, --repo REPO  git repository to be used
  -v, --verbose         increase output verbosity
```

## Requirements

- Python3

```bash
pip install -r requirements.txt
```
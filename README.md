# Yggdrasil

Yggdrasil is a project named after [the Norse tree of life](https://en.wikipedia.org/wiki/Yggdrasil). It is basically adding an API layer over [Ollama](https://ollama.com/) deployed on top of [Kubernetes](https://kubernetes.io). The API is responsible to receive multiple prompts and perform some functions such as similarity, offensive contents detection and handling them.

```mermaid
flowchart LR
    A(API) --> B(Ollama)
```

## Prerequisites

To get started with, the following items are required:

- [Kind](https://kind.sigs.k8s.io/)
- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)

## Quick start

To get started run the following:

```bash
git clone git@github.com:dinateimouri/yggdrasil.git

./scripts/startup.sh
```


## Cleanup

To remove all packages run the following:

```bash
./scripts/cleanup.sh
```

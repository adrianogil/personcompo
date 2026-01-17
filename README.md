# personcompo

Modeling personality as a composition of behaviors for game AI agents.

## Overview

This repository contains a small framework for combining weighted behaviors into a single
agent policy, plus a sample dominoes simulation that exercises the framework. Behaviors
contribute utility scores for candidate actions, and agents pick the lowest-scoring action
at each decision point.

## Project layout

- `src/python/personcompo/framework`: Core agent + behavior abstractions.
- `src/python/personcompo/dominoes`: Sample dominoes game and behavior implementations.
- `src/bashrc.sh`: Shell helper for setting local environment variables.

## Requirements

- Python 3.8+ (managed via Poetry)
- No third-party runtime dependencies (stdlib only)

## Setup with Poetry

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Install dependencies:

```bash
poetry install
```

3. (Optional) Activate the virtual environment:

```bash
poetry shell
```

## Running the dominoes simulation

From the repository root:

```bash
poetry run python -m personcompo.dominoes.dominoesgame
```

You can also pass a number of games to simulate, or enable debug output:

```bash
poetry run python -m personcompo.dominoes.dominoesgame 10
poetry run python -m personcompo.dominoes.dominoesgame --details
```

## Extending the framework

- Implement a new behavior by defining `update_world_state` and `eval` methods.
- Register the behavior on a `GameAgent` with a weight via `add_behavior`.
- Wire the agent into a game loop (see `DominoesGame` for a reference implementation).

## Roadmap ideas

- Add additional games for benchmarking behavior compositions.
- Provide a training loop for learning behavior weights.
- Add tests for deterministic simulation scenarios.

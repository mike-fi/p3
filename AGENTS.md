<INSTRUCTIONS>
## Overview
This repository uses `uv` for dependency and environment management and targets Python development, including a pytest plugin.
Follow the guidelines below when editing or adding code.

## Workflow
- Use `uv` for running tools: `uv run <tool>` or `uv run python -m <tool>` as appropriate.
- Prefer small, focused changes with clear, testable behavior.
- Keep compatibility with the supported Python versions declared in `pyproject.toml`.

## Code Style
- Format and lint with `ruff`:
  - Format: `uv run ruff format .`
  - Lint: `uv run ruff check .`
- Prefer explicit, readable code over cleverness.
- Keep functions small and focused.
- Avoid new dependencies unless necessary.

## Type Checking
- Use `ty` for static checks:
  - `uv run ty check .`
- Add type annotations for public APIs and complex logic.
- Keep types accurate and avoid `Any` unless unavoidable.

## Testing
- Use `pytest` for tests:
  - `uv run pytest`
- When changing plugin behavior, add or update tests under `tests/`.
- If a change affects public API, update or add regression tests.

## Pre-commit Hooks
- If pre-commit is installed, run:
  - `uv run pre-commit run --all-files`
- Do not bypass hooks unless a failure is understood and addressed.

## Common Commands
- Install dependencies: `uv sync`
- Run tests: `uv run pytest`
- Format: `uv run ruff format .`
- Lint: `uv run ruff check .`
- Type check: `uv run ty check .`

## Python Plugin Notes
- Ensure pytest hooks are registered correctly in the plugin package.
- Keep plugin behavior deterministic and side-effect minimal.
- Avoid global state where possible.
</INSTRUCTIONS>

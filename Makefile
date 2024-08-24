## All these commands except venv assume you are in a venv

## Default path vor uv.
VENV_NAME = .venv

venv:
	uv venv

install: venv
	uv sync --all-extras
	uv run pre-commit install

fix:
	uv run pre-commit run --all-files

test:
	uv run pytest --cov=src/structured_llm_templates --cov-report=term-missing

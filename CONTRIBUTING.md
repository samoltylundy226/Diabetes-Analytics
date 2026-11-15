# Contributing Guidelines

Thank you for your interest in contributing to **Diabetes Healthcare Analytics**!

## Workflow

1. Fork or branch from `main` using a descriptive branch name (for example, `feature/eda-visualizations` or `fix/preprocessing-validation`).
2. Keep raw data immutable: never overwrite or commit modified files into `data/raw/`.
3. Follow PEP 8 style guidelines and write clear docstrings for new functions and modules.
4. Use relative paths via `pathlib.Path` rather than hardcoded absolute system paths.
5. Add or update unit tests in `tests/` for any changes to `src/` logic and run `pytest` before committing.
6. Ensure every notebook code cell has an accompanying markdown explanation cell and clear outputs before committing large renders if needed.
7. Never commit credentials, `.env` files, or sensitive information.

## Commit Message Style

Use concise, imperative commit messages describing the change:

- `Add BMI distribution analysis in EDA module`
- `Fix blood pressure validation rule in preprocessing`
- `Update data dictionary with clinical range notes`

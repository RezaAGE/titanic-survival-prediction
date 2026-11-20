# Contributing

Thank you for your interest in improving this educational Titanic classification project.

## Code-preservation policy

This GitHub edition is intentionally **source-preserving**: the 43 executable Python cells in `Notebooks/Titanic.ipynb` must remain unchanged. Contributions limited to documentation, figures, tests and repository metadata are welcome under this constraint.

For a future experiment that changes the pipeline, please propose a **separately labeled variant** rather than silently replacing the historical notebook or its saved evaluation.

## Before opening a pull request

1. Explain the problem and the proposed scope.
2. Run `python scripts/validate_project.py`.
3. Run `python -m unittest discover -s tests -v`.
4. Document whether your change touches data, code, Markdown, outputs or provenance.
5. Never claim a new score unless backed by a reproducible experiment or external evaluation.
6. Do not add machine-local paths, cache directories, personal credentials or generated training logs.

Dataset files are not covered by the repository's MIT license; review [data provenance](docs/DATA_PROVENANCE.md) before changing or redistributing them.

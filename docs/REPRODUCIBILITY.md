# Running and Validating the Project

## 1. Project layout requirements

Keep the data directory next to `Notebooks/`:

```text
repo-root/
├── Data/
│   ├── train.csv
│   └── test.csv
└── Notebooks/
    └── Titanic.ipynb
```

The existing notebook literally references `r"..\Data\train.csv"` and `r"..\Data\test.csv"`. Because its code must remain unchanged, **run it on Windows from `Notebooks/`** so these paths resolve correctly. They may fail on Linux/macOS even if the repository structure is correct.

## 2. Environment and dependencies

The notebook's original kernel metadata reports **Python 3.14.7**. The archive did **not** provide an exact `pip freeze`, environment lockfile, or verified list of installed versions. `requirements.txt` is therefore a reasonable direct-dependency declaration, **not** a reproduction of the original machine's exact package versions.

From the repository root in PowerShell:

```powershell
py -3.14 --version
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If Python 3.14 is not installed, use a compatible Python interpreter available on your system (for example, Python 3.12) but note that package and model behavior may vary. In particular, LazyPredict and its optional model dependencies may have version-specific compatibility constraints. **The package installation and notebook rerun were not tested during packaging.**

## 3. Static, no-training validation

From the repository root:

```powershell
python scripts/validate_project.py
python -m unittest discover -s tests -v
```

Both commands use **only the Python standard library**. They verify:

- Notebook JSON shape and valid code-cell count.
- **SHA-256 digest of each original executable source cell**, plus the concatenated code-cell manifest.
- Presence of every required input and output artifact.
- Training and test CSV column names, row count and uniqueness of passenger IDs.
- The training label domain (`0`/`1`).
- The saved submission's column order, binary predictions, row count and exact alignment with test passenger identifiers.
- SHA-256 byte checks of both original data CSVs and the original submission snapshot.
- The existence of the English final report and auxiliary documentation.

**They do not:** import `lazypredict`, fit models, verify numerical reproducibility of a fresh run, or assert an external competition score.

## 4. Run the notebook

In the same activated environment:

```powershell
cd Notebooks
python -m ipykernel install --user --name titanic-project --display-name "Python (Titanic Project)"
jupyter lab Titanic.ipynb
```

Choose the **Python (Titanic Project)** kernel and execute cells in their original top-to-bottom order. Features are derived before the holdout split and the 132-candidate grid search contains 660 fits. The saved notebook result cells remain visible for reference.

The final code cell writes `submission.csv` to the current working directory, normally `Notebooks/`. This generated file is ignored by Git. The original supplied submission is kept at `outputs/submission.csv` for evidence and comparison.

**Do not assume identical metrics after dependency upgrades**; model implementations, defaults, warnings and available LazyPredict candidate estimators may change.

## 5. Files, outputs and provenance

| Artifact | Origin | Status |
|---|---|---|
| `Data/train.csv` | Source archive | Preserved byte-for-byte |
| `Data/test.csv` | Source archive | Preserved byte-for-byte |
| `Notebooks/Titanic.ipynb` executable cells | Source archive | **Unchanged Python source**; Markdown enriched |
| `Notebooks/Titanic.ipynb` saved outputs | Source archive | Substantive outputs preserved; machine-specific warning streams removed |
| `outputs/submission.csv` | Source `Notebooks/submission.csv` | Preserved byte-for-byte, relocated to avoid generated-file clutter |
| `assets/` | This GitHub edition | Original charts and graphics calculated from supplied data/saved metrics |
| `docs/recorded_metrics.json` | This GitHub edition | Arithmetic from original stored matrix and scores |

The original archive also included `Notebooks/catboost_info/` training telemetry, which is excluded from the publication-ready ZIP because it is an automatically generated intermediate artifact.

## 6. Troubleshooting

| Symptom | Likely cause | Check / response |
|---|---|---|
| `FileNotFoundError` for `..\Data\train.csv` | Notebook started from the wrong directory | `import os; print(os.getcwd())` should point at `...\Notebooks` |
| `ModuleNotFoundError` for `category_encoders` or `lazypredict` | Dependencies absent from the selected Jupyter kernel | Confirm kernel, then install from `requirements.txt` in that environment |
| Kernel doesn't match environment | Notebook using a different Python kernel | Register/select `Python (Titanic Project)` |
| Long grid search | 660 fits and multiple solvers, using parallel jobs | This is expected for the original search; static checks do not retrain |
| Deprecation / future warnings | Matplotlib/scikit-learn API changes | Documented in [Engineering Notes](ENGINEERING_NOTES.md); Python code intentionally unchanged |
| Unexpected fresh-run scores | Version drift, nondeterministic fitting, modeling caveats | Record library versions and compare with saved outputs; don't claim guaranteed exact reproduction |
| Linux/macOS data-load failure | Literal Windows backslashes | The unmodified notebook requires Windows-compatible execution; static QA remains cross-platform |

## 7. Integrity contract

The manifest `notebook-code-manifest.json` records the source hashes of the original **43 executable cells**. The validator recomputes those digests from `Notebooks/Titanic.ipynb` and fails if even one code cell source changes.

This means a user may add or edit Markdown without violating the original code-preservation contract, while modification, removal, insertion or reordering of executable code will be detected.

See [Release Notes](RELEASE_NOTES.md) for the exact repository-level changes.

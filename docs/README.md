# Documentation Center

This directory contains the evidence-based documentation for **Titanic Survival Prediction**. The reference experiment is the supplied `Notebooks/Titanic.ipynb`; no new model training was carried out when producing this GitHub-ready edition.

| Document | Contents |
|---|---|
| **[FINAL_REPORT.md](FINAL_REPORT.md)** | Executive summary, problem, data, workflow, saved results, interpretation, and research limitations |
| **[FINAL_REPORT.pdf](FINAL_REPORT.pdf)** | Six-page visually designed companion report with the principal results and caveats |
| [METHODOLOGY.md](METHODOLOGY.md) | Exact feature-engineering logic, preprocessing, model selection and 5-fold tuning settings |
| [MODEL_CARD.md](MODEL_CARD.md) | Intended use, model description, metrics, limitations, and risk considerations |
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Raw Titanic columns and exact definitions of engineered features |
| [DATA_PROVENANCE.md](DATA_PROVENANCE.md) | Dataset scope, evidence and publication/attribution caveats |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | Local Windows setup, execution order, testing, artifact outputs and failure guidance |
| [ENGINEERING_NOTES.md](ENGINEERING_NOTES.md) | Known methodological and technical limitations with proposed next steps |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | Exact file preservation and documentation changes compared with the supplied archive |
| [recorded_metrics.json](recorded_metrics.json) | Machine-readable figures derived from the original saved outputs |

**Evidence levels:**

- **Directly verified:** contents of `Data/train.csv` and `Data/test.csv`, original notebook source cells, stored notebook result outputs, saved `submission.csv`.
- **Arithmetically derived:** percentages and positive-class metrics computed from the saved confusion matrix.
- **Not independently verified:** successful fresh training under a new environment, a Kaggle leaderboard score, independent test accuracy, exact dependency-version lockfile, external origin or license of the raw CSV files.

Return to [project homepage](../README.md).

# Data Provenance, Attribution and Publication Review

## What was included

The user-provided project archive contained `Data/train.csv` and `Data/test.csv`, with **891** and **418** rows respectively, plus a notebook using those files and a generated submission snapshot.

The input fields and split are consistent with the familiar **Kaggle Titanic — Machine Learning from Disaster** benchmark:

<https://www.kaggle.com/competitions/titanic/data>

However, this archive does **not** include records proving when, where, or under what terms these exact files were downloaded. The dataset source is therefore described as a **schema match**, rather than as an independently verified acquisition record.

## Reuse and publication

- Retain the attribution link in README and reports.
- Before making a **public** GitHub repository, the repository owner should verify that publishing the exact CSV files is consistent with the dataset/competition terms they accepted.
- The project's `LICENSE` is an MIT license for authored **project code and project documentation/visualizations**, not a license grant for third-party Titanic CSV contents.
- If redistribution cannot be confirmed, remove only `Data/train.csv` and `Data/test.csv` from the *public release*, and document the official download process. The unchanged notebook still expects those files locally under `Data/`.
- No passenger label predictions should be presented as ground truth.

## Integrity scope

The release validator checks row counts, schema, labels, identifiers and prediction relationships. Its expectations describe **the supplied snapshot**, not an eternal guarantee that every future version of this benchmark will have the same shape.

This document addresses attribution of the dataset files only. The original notebook's Python code is separately protected by SHA-256 source-cell hashes.

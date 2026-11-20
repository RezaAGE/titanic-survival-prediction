#!/usr/bin/env python3
"""Validate the published Titanic repository without installing ML packages.

Checks notebook-code preservation using an authoring-time SHA-256 manifest,
input CSV layout, binary labels, saved output mapping and required documents.
This script deliberately does not execute or modify the source notebook.

Usage (from any directory):
    python scripts/validate_project.py

Exit status: 0 when all checks pass; 1 on a failed or unreadable check.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRAIN_FIELDS = (
    'PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age',
    'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked',
)
TEST_FIELDS = tuple(column for column in TRAIN_FIELDS if column != 'Survived')
SUBMISSION_FIELDS = ('PassengerId', 'Survived')


def check(condition: bool, explanation: str) -> None:
    """Raise an actionable error rather than relying on disabled-able assert."""
    if not condition:
        raise ValueError(explanation)
    print(f'[PASS] {explanation}')


def load_json(relative_path: str) -> dict:
    """Load a UTF-8 JSON document relative to the repository root."""
    with (ROOT / relative_path).open('r', encoding='utf-8') as handle:
        return json.load(handle)


def load_csv(relative_path: str) -> tuple[list[str], list[dict[str, str]]]:
    """Read a small repository CSV without requiring pandas."""
    with (ROOT / relative_path).open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        if fields is None:
            raise ValueError(f'{relative_path} does not have a header')
        return fields, list(reader)


def validate_notebook() -> None:
    """Confirm that the 43 original code cell sources match the manifest."""
    notebook = load_json('Notebooks/Titanic.ipynb')
    manifest = load_json('notebook-code-manifest.json')
    check(notebook.get('nbformat') == 4, 'Notebook uses nbformat 4')
    cells = notebook.get('cells')
    check(isinstance(cells, list), 'Notebook contains a valid cells list')
    check(all(c.get('cell_type') in {'markdown', 'code', 'raw'} for c in cells), 'Notebook cell types are supported')
    cell_ids = [c.get('id') for c in cells]
    check(all(isinstance(i, str) and i for i in cell_ids) and len(set(cell_ids)) == len(cell_ids),
          'Notebook cells have unique, nonempty IDs')

    code_cells = [c for c in cells if c['cell_type'] == 'code']
    check(len(code_cells) == manifest['code_cell_count'] == 43, 'All 43 original code cells are present')
    sources = []
    for index, cell in enumerate(code_cells):
        source = cell.get('source', [])
        check(isinstance(source, (list, str)), f'Code cell {index+1} source has valid type')
        text = ''.join(source) if isinstance(source, list) else source
        sources.append(text)
        actual = hashlib.sha256(text.encode('utf-8')).hexdigest()
        expected = manifest['individual_code_cell_sha256'][index]
        if actual != expected:
            raise ValueError(f'Code cell {index+1} was changed. SHA-256 does not match baseline.')
    joined = json.dumps(sources, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    check(hashlib.sha256(joined).hexdigest() == manifest['code_sources_sha256'],
          'Full ordered Python code signature matches the source archive')
    check(sum(c['cell_type'] == 'markdown' for c in cells) >= manifest['original_markdown_cell_count'],
          'All original Markdown sections have been retained and expanded')
    print(f'[INFO] {len(cells)} cells, {len(code_cells)} original Python cells, SHA-256 integrity verified')


def unique_integer_ids(rows: list[dict[str, str]], label: str) -> list[int]:
    """Ensure each row has a valid and distinct integer passenger identifier."""
    ids = []
    for row_number, row in enumerate(rows, 2):
        try:
            ids.append(int(row['PassengerId']))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'{label} has an invalid PassengerId on CSV line {row_number}') from exc
    check(len(ids) == len(set(ids)), f'{label} has no duplicate PassengerId values')
    return ids


def validate_data_and_submission() -> None:
    """Check exact supplied snapshot schemas and test/output relationships."""
    train_headers, train = load_csv('Data/train.csv')
    test_headers, test = load_csv('Data/test.csv')
    submission_headers, submission = load_csv('outputs/submission.csv')
    check(tuple(train_headers) == TRAIN_FIELDS, 'Train CSV has expected 12-column schema and order')
    check(tuple(test_headers) == TEST_FIELDS, 'Test CSV has expected 11-column schema and order')
    check(tuple(submission_headers) == SUBMISSION_FIELDS, 'Submission contains exactly PassengerId and Survived')
    check(len(train) == 891, 'Train CSV contains 891 passengers')
    check(len(test) == 418, 'Test CSV contains 418 passengers')
    check(len(submission) == 418, 'Submission contains 418 passenger predictions')

    train_ids = unique_integer_ids(train, 'train.csv')
    test_ids = unique_integer_ids(test, 'test.csv')
    submission_ids = unique_integer_ids(submission, 'submission.csv')
    check(not (set(train_ids) & set(test_ids)), 'Training and test identifiers do not overlap')
    check(submission_ids == test_ids, 'Submission IDs match test CSV exactly in row order')
    check(all(row['Survived'] in {'0', '1'} for row in train), 'Training survival labels are binary')
    check(all(row['Survived'] in {'0', '1'} for row in submission), 'Submission predictions are binary')

    positives = sum(row['Survived'] == '1' for row in train)
    check(positives == 342, 'Training label balance matches source: 342 survivors')
    predicted = sum(row['Survived'] == '1' for row in submission)
    check(predicted == 175, 'Submission snapshot matches source: 175 predicted survivors')
    print(f'[INFO] Dataset sizes: train={len(train)}, test={len(test)}, submission={len(submission)}')


def validate_source_artifact_hashes() -> None:
    """Confirm that source CSV snapshots still match the original package."""
    manifest = load_json('notebook-code-manifest.json')
    hashes = manifest['source_artifact_sha256']
    for relative_name, reference_digest in hashes.items():
        actual_digest = hashlib.sha256((ROOT / relative_name).read_bytes()).hexdigest()
        check(actual_digest == reference_digest, f'{relative_name} matches original SHA-256 snapshot')


def validate_documents() -> None:
    """Check essential documentation and asset inventory."""
    must_exist = (
        'README.md', 'LICENSE', 'CONTRIBUTING.md', 'requirements.txt',
        '.gitignore', '.gitattributes', '.editorconfig',
        '.github/workflows/quality.yml',
        'docs/README.md', 'docs/FINAL_REPORT.md', 'docs/FINAL_REPORT.pdf', 'docs/METHODOLOGY.md',
        'docs/DATA_DICTIONARY.md', 'docs/DATA_PROVENANCE.md',
        'docs/MODEL_CARD.md', 'docs/REPRODUCIBILITY.md',
        'docs/ENGINEERING_NOTES.md', 'docs/RELEASE_NOTES.md',
        'assets/project-banner.svg', 'assets/pipeline-overview.svg',
        'assets/validation-confusion-matrix.png',
        'assets/survival-distribution.png', 'assets/missingness.png',
    )
    absent = [name for name in must_exist if not (ROOT / name).is_file()]
    check(not absent, f'Required documents/assets exist ({len(must_exist)} paths)')
    metrics = load_json('docs/recorded_metrics.json')
    check(metrics.get('confusion_matrix') == [[116, 21], [18, 68]],
          'Recorded model evaluation retains source confusion matrix')
    check(metrics.get('kaggle_leaderboard_score') is None,
          'No unverified Kaggle leaderboard score is claimed')


def main() -> int:
    print(f'Titanic repository static validation — {ROOT}')
    try:
        validate_notebook()
        validate_data_and_submission()
        validate_source_artifact_hashes()
        validate_documents()
    except (ValueError, FileNotFoundError, OSError, KeyError, IndexError, TypeError,
            json.JSONDecodeError, csv.Error) as exc:
        print(f'[FAIL] {exc}', file=sys.stderr)
        return 1
    print('\nAll static repository checks passed. No model retraining was performed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

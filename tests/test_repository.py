"""Dependency-free tests for dataset integrity and original notebook source.

Run from repository root: python -m unittest discover -s tests -v
These checks are not a replacement for retraining or a leaderboard result.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: str):
    with (ROOT/path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


class RepositoryIntegrityTests(unittest.TestCase):
    """Regression checks for content that must remain stable in this release."""

    def test_source_code_digest_and_count(self):
        notebook = json.loads((ROOT/'Notebooks/Titanic.ipynb').read_text(encoding='utf-8'))
        manifest = json.loads((ROOT/'notebook-code-manifest.json').read_text(encoding='utf-8'))
        code = [''.join(c['source']) if isinstance(c['source'], list) else c['source']
                for c in notebook['cells'] if c['cell_type'] == 'code']
        self.assertEqual(43, len(code))
        self.assertEqual(len(code), len(manifest['individual_code_cell_sha256']))
        self.assertEqual([
            hashlib.sha256(source.encode('utf-8')).hexdigest() for source in code
        ], manifest['individual_code_cell_sha256'])
        signature = hashlib.sha256(json.dumps(code, ensure_ascii=False,
                                             separators=(',', ':')).encode('utf-8')).hexdigest()
        self.assertEqual(signature, manifest['code_sources_sha256'])

    def test_labeled_data_matches_expected_snapshot(self):
        train = read_csv('Data/train.csv')
        self.assertEqual(len(train), 891)
        self.assertEqual(sum(row['Survived'] == '1' for row in train), 342)
        self.assertEqual(len({row['PassengerId'] for row in train}), len(train))
        self.assertEqual(sum(not row['Age'] for row in train), 177)
        self.assertEqual(sum(not row['Cabin'] for row in train), 687)

    def test_unlabeled_test_set_matches_expected_snapshot(self):
        test = read_csv('Data/test.csv')
        self.assertEqual(len(test), 418)
        self.assertNotIn('Survived', test[0])
        self.assertEqual(len({row['PassengerId'] for row in test}), len(test))
        self.assertEqual(sum(not row['Age'] for row in test), 86)
        self.assertEqual(sum(not row['Fare'] for row in test), 1)

    def test_submission_preserves_test_order_and_binary_domain(self):
        test = read_csv('Data/test.csv')
        submission = read_csv('outputs/submission.csv')
        self.assertEqual(418, len(submission))
        self.assertEqual([r['PassengerId'] for r in test],
                         [r['PassengerId'] for r in submission])
        self.assertEqual({'0', '1'}, {r['Survived'] for r in submission})
        self.assertEqual(175, sum(r['Survived'] == '1' for r in submission))

    def test_recorded_validation_metrics_match_confusion_matrix(self):
        metrics = json.loads((ROOT/'docs/recorded_metrics.json').read_text(encoding='utf-8'))
        self.assertEqual([[116, 21], [18, 68]], metrics['confusion_matrix'])
        self.assertAlmostEqual(184/223, metrics['validation_accuracy'])
        self.assertAlmostEqual(68/(68+21), metrics['positive_precision'])
        self.assertAlmostEqual(68/(68+18), metrics['positive_recall'])
        self.assertIsNone(metrics['kaggle_leaderboard_score'])

    def test_original_csv_bytes_match_source_manifest(self):
        manifest = json.loads((ROOT/'notebook-code-manifest.json').read_text(encoding='utf-8'))
        for relative_path, expected in manifest['source_artifact_sha256'].items():
            with self.subTest(file=relative_path):
                actual = hashlib.sha256((ROOT/relative_path).read_bytes()).hexdigest()
                self.assertEqual(expected, actual)

    def test_cli_static_validation(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/validate_project.py')],
                                cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, msg=result.stdout+'\n'+result.stderr)


if __name__ == '__main__':
    unittest.main()

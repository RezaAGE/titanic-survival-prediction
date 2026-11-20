# Model Card — Titanic Survival Logistic Regression

## Model overview

| Field | Description |
|---|---|
| Task | Binary classification of Titanic passenger survival labels |
| Predicted outcome | `Survived` = `0` or `1` |
| Final model family | Scikit-learn regularized logistic regression |
| End-to-end estimator | `Pipeline(ColumnTransformer, LogisticRegression)` |
| Model selection | Five-fold `GridSearchCV`, weighted F1 |
| Saved optimal settings | `C=1`, `class_weight=None`, `l1_ratio=1`, `solver='saga'` |
| Training subset | 668 rows of the 891-row labeled dataset |
| Local validation subset | 223 stratified holdout rows |
| Competition test set | 418 unlabeled rows; prediction-only |
| Source artifact | `Notebooks/Titanic.ipynb` |
| Serialized model included? | **No** (the project contains code and a saved submission, not an exported model binary) |

## Intended use

- Educational demonstrations of data preparation, feature engineering, categorical transformations, regularized linear classifiers and local evaluation.
- Portfolio presentation and reproducible examination of a classical tabular competition problem.

## Out-of-scope or unsuitable use

- Prediction about real people in consequential travel, rescue, medical, financial, employment, or safety decisions.
- Claims about causality, historical counterfactuals, or policy interventions.
- Claims about population-level fairness or generalization outside the provided benchmark.
- Statements about performance on the unlabeled competition test set or Kaggle leaderboard without external evaluation evidence.

## Evaluation

**Observed holdout confusion matrix:** `[[116,21],[18,68]]`, rows true labels and columns predicted labels.

| Metric | Saved or derived value |
|---|---:|
| Accuracy | 82.51% |
| Class 1 precision | 76.40% |
| Class 1 recall | 79.07% |
| Class 1 F1 | 77.71% |
| Best 5-fold CV weighted F1 | 0.8218763593 |
| Kaggle score | Not provided / not verified |

The holdout has **137 class-0** and **86 class-1** records. The classifier incorrectly predicts survival for 21 non-survivors and incorrectly predicts non-survival for 18 survivors. Positive-class recall is consequently approximately 79.07%.

## Input features and transformations

`Sex` is ordinal-encoded. `Embarked`, `Title`, and `CabinDeck` are one-hot encoded. `TicketPrefix` is count-encoded and standardized. A collection of numeric and engineered predictors is standardized, while remaining binary indicators are passed through. See [Methodology](METHODOLOGY.md) and [Data Dictionary](DATA_DICTIONARY.md).

## Known limitations

1. Group-level imputation occurs **before** the train/validation split, allowing the validation feature distribution to influence imputation statistics.
2. The final reported holdout was also consulted during earlier algorithm screening; estimates may be optimistic due to model selection.
3. Training and test CSVs are imputed separately; there is no persisted fit-only imputation step.
4. The dataset is small and reflects an unusual historical event, so external validity is limited.
5. Features such as sex, class and age carry social and demographic information and warrant careful interpretation. No dedicated fairness analysis appears in the original notebook.
6. The classifier is not accompanied by uncertainty estimates, probability calibration measurements, deployment monitoring, or a tested external validation cohort.
7. No serialized estimator or complete environment lockfile is included.

## Traceability

The numbers above are extracted from saved notebook outputs or directly calculated from the saved confusion matrix. No fresh model retraining was performed for this GitHub edition. The original Python sources are protected by [`notebook-code-manifest.json`](../notebook-code-manifest.json).

See [Final Report](FINAL_REPORT.md) for a complete evaluation discussion.

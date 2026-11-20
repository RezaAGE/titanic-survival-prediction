# Engineering Notes: Known Limitations and Improvement Plan

**Preservation principle:** no executable code in `Notebooks/Titanic.ipynb` was rewritten in this release. These observations therefore distinguish *current implementation* from *potential future work*.

## A. Methodology

### A1. Grouped imputation occurs before the validation split

**Observed:** `train_df=median_group_imputer(...)`, `mode_group_imputer(...)`, and `mean_group_imputer(...)` run before `train_test_split`.

**Why it matters:** imputation medians/means/modes are estimated from the full 891-row labeled dataset's predictors, including the 223 later-selected validation rows. This is feature-statistic leakage and means the later validation process is not completely isolated from preparation decisions.

**Future change (not implemented):** perform the split first and fit group-based imputers within a scikit-learn-compatible transformer inside the cross-validated pipeline. Define training-derived fallback values for entirely missing groups.

### A2. Test-set imputations are fitted on the test set

**Observed:** `median_group_imputer(test_df, ...)` uses test-frame groups, and analogously for the other imputation functions.

**Why it matters:** a production inference pipeline normally reuses imputation statistics learned from labeled training predictors. Test-frame-specific statistics make predictions partly dependent on which unlabeled rows happen to be processed together.

**Future change:** persist training-side imputation statistics and apply them consistently at inference time.

### A3. Holdout reuse during algorithm screening

**Observed:** LazyPredict evaluates on `X_val_transformed, y_val`; the tuned logistic-regression pipeline is evaluated on `X_val, y_val` afterward.

**Why it matters:** choosing a model family after inspecting holdout rankings reduces the independence of the reported validation score, even though grid search itself uses the training subset and separate CV folds.

**Future change:** use nested CV or a separate untouched final test partition.

### A4. Comparability of metrics

**Observed:** LazyPredict reports multiple metrics, grid search uses `f1_weighted`, and the final report prints accuracy/precision/recall/F1 with a confusion matrix.

**Why it matters:** **mean fold weighted F1 ≠ validation accuracy ≠ leaderboard score**. These must never be conflated.

## B. Code and portability

| Issue | Current source behavior | Proposed change (not applied) |
|---|---|---|
| Windows-specific file paths | `r"..\Data\train.csv"` and `r"..\Data\test.csv"` | Use `pathlib` / consistent project-root resolution |
| Row-wise feature engineering | Multiple explicit row loops | Vectorize while adding robust input tests |
| Ticket parser edge cases | `int(ticket_number)` can raise on unexpected strings | Defensive parsing with clear unknown/invalid categories |
| Empty group mode | `x.mode()[0]` assumes a nonempty mode | Fall back to global training mode |
| Entirely null groups | Group mean/median can remain null | Fit global fallback only on training folds |
| Category handling | Ordinal encoding has default unknown-category behavior | Explicit unknown-value policy |
| Matplotlib deprecation | `boxplot(..., vert=False)` | Use a version-appropriate supported orientation API |
| LogisticRegression future warning | Explicit `n_jobs=-1` parameter | Remove unsupported parameter when changing code is allowed |
| Dependency drift | No exact installed-version snapshot | Record tested package versions and create a lockfile |
| Testability | Notebook runs long grid search interactively | Factor core pipeline into separately testable components |

The static CI intentionally does not attempt to execute the unchanged Windows-path notebook on Linux or rerun 660 cross-validation fits.

## C. Data / model governance

- **Data rights:** independently verify that bundled benchmark CSVs may be redistributed publicly.
- **Historical/demographic context:** associations involving sex and passenger class should not be generalized or interpreted as causal or morally neutral measures.
- **Reproducible evaluation:** record software versions, fold-level statistics, and any public-score feedback only after those exist.
- **Uncertainty:** measure repeated-split or bootstrap intervals, and consider calibrated class probabilities if the research question calls for it.

## D. Suggested order for a later code revision

1. Agree that executable notebook changes are permitted; current release explicitly forbids them.
2. Move source loading to platform-independent paths and add parser fallbacks.
3. Build fit-on-train-only imputers within the preprocessing pipeline.
4. Redesign model selection with an independent outer evaluation protocol.
5. Rerun and report updated metrics; **do not replace stored historical values** without labeling a new experiment.
6. Add dependency lockfile, notebook smoke tests, automated modeling checks and experiment tracking.

No item in this proposed plan is marked complete in this release.

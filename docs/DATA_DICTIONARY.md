# Data Dictionary

**Input schema:** `Data/train.csv` has 12 fields; `Data/test.csv` has the same fields **except `Survived`**. Both are provided in the uploaded project, not fetched by an external tool when constructing this release.

## Original columns

| Column | Data type in supplied CSV | Role | Notes |
|---|---|---|---|
| `PassengerId` | Integer | Unique identifier | Excluded from predictors; preserved for submission |
| `Survived` | Integer 0/1 | Target (train only) | `0` = non-survivor, `1` = survivor |
| `Pclass` | Integer | Predictor | Ticket class, encoded/scaled as numeric in the notebook |
| `Name` | Text | Source feature | Used to extract `Title`, then dropped |
| `Sex` | Text | Predictor | Ordinal-encoded categorical field |
| `Age` | Decimal | Predictor | Group median imputation; initial missingness flagged |
| `SibSp` | Integer | Source feature | Number of siblings/spouses aboard; used to construct family features, then dropped |
| `Parch` | Integer | Source feature | Number of parents/children aboard; used to construct family features, then dropped |
| `Ticket` | Text | Source feature | Parsed into prefix, number and length, then dropped |
| `Fare` | Decimal | Source feature | Converted to `FareLog`, then dropped |
| `Cabin` | Text | Source feature | Converted to deck and count, then dropped |
| `Embarked` | Text | Predictor | Port code: `C`, `Q`, or `S`; grouped mode imputation |

The original dataset uses standard Titanic benchmark conventions. The source archive does not include a separate formal dataset license or data-acquisition provenance record.

## Engineered columns

| Engineered field | Computation or encoding | Type after feature creation | Special handling |
|---|---|---|---|
| `Title` | Honorific extraction: `Mr`, `Mrs`, `Miss`, `Master`, `Rare` | Categorical text | One-hot encoded |
| `TicketPrefix` | Uppercase and strip selected punctuation from ticket prefix | Categorical text | Count-encoded, then scaled |
| `TicketNumber` | `ln(parsed_numeric_token+1)` | Numeric | Standardized |
| `TicketLength` | `len(original Ticket string)` | Integer | Standardized |
| `CabinDeck` | First letter of cabin or `Unknown` | Categorical text | One-hot encoded |
| `CabinCount` | Number of space-separated cabin references, or `0` | Integer | Standardized |
| `FamilySize` | `SibSp + Parch + 1` | Integer | Standardized |
| `IsAlone` | `1` when `SibSp + Parch == 0`, else `0` | Binary integer | Passed through |
| `AgeMissing` | `1` when original `Age` is null, else `0` | Binary integer | Passed through |
| `FareLog` | `ln(Fare+1)` | Numeric | Group mean imputation if null; standardized |

`Pclass` and `Age` remain model inputs. `Embarked` and `Sex` are encoded. `PassengerId` and `Survived` never enter the predictor matrix.

## Observed missingness

| Field | Train missing | Test missing |
|---|---:|---:|
| `Age` | 177 | 86 |
| `Cabin` | 687 | 327 |
| `Embarked` | 2 | 0 |
| `Fare` | 0 | 1 |

All other original input columns are complete in the provided snapshots. For exact validation, run `python scripts/validate_project.py` from the repository root.

## Submission schema

| Column | Data type | Expected rule |
|---|---|---|
| `PassengerId` | Integer | Exactly matches each `Data/test.csv` identifier in source order |
| `Survived` | Integer | Prediction must be `0` or `1` |

The stored `outputs/submission.csv` contains 418 rows (243 zeros and 175 ones). Its predictions are model outputs, not ground-truth labels.

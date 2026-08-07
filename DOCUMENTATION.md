# Anemia Prediction System — Technical Documentation

## 1. Overview

**Anemia Prediction System** is an end-to-end Machine Learning system that predicts the presence of anemia in a patient based on five hematological variables: gender, hemoglobin, MCH, MCHC, and MCV.

The project covers the complete model lifecycle:

* Exploratory analysis and preprocessing of clinical data.
* Feature engineering based on medical domain knowledge.
* Comparison of seven binary classification algorithms.
* Selection and interpretability of the final model (CatBoost).
* Model deployment through a REST API (FastAPI).
* Persistence of each prediction in a SQLite database.

The clinical use case prioritizes **recall**: in a diagnostic problem, a false negative (an anemic patient classified as healthy) is the most costly error, so recall was used as the primary metric for model selection, with F1-Score, accuracy, and precision as complementary metrics.

> ⚠️ **Disclaimer:** *project developed for educational purposes as part of a Data Science portfolio. It is not a certified medical device and should not be used to make real clinical decisions without the supervision of a healthcare professional. The dataset used (1,421 records) is limited in origin and size and has not undergone external clinical validation.*

## 2. Project Structure

```text
Anemia-Prediction-System/
├── api/                    # REST API (FastAPI)
│   ├── main.py             # App and endpoint definitions
│   ├── config.py           # API configuration and metadata
│   ├── loader.py           # Serialized pipeline loading
│   ├── predict.py          # Inference logic
│   └── schemas.py          # Pydantic models (request/response)
├── database/               # Persistence (SQLAlchemy + SQLite)
│   ├── database.py         # Engine, session, and database creation
│   ├── tables.py           # ORM model `Prediction`
│   ├── crud.py             # Read/write operations
│   ├── config.py           # Database path and URL
│   └── anemia.db           # SQLite database
├── src/                    # Reusable ML code
│   ├── preprocessing/
│   │   └── features.py     # Transformers: FeatureEngineering, FeatureSelector
│   └── models/
│       └── evaluate.py     # Model evaluation utilities
├── models/                 # Trained artifacts (.pkl)
│   ├── catboost_pipeline.pkl    # Complete pipeline used in production
│   ├── catboost_model.pkl       # Standalone CatBoost model
│   ├── final_preprocessor.pkl   # Final preprocessor
│   ├── preprocessor.pkl         # Preprocessor (intermediate version)
│   └── preprocessor_pipeline.pkl # Preprocessing pipeline
├── data/
│   ├── raw/anemia.csv       # Original dataset (1,421 records)
│   └── processed/           # Train/validation/test splits in .npy format
├── notebooks/               # Data Science workflow
│   ├── 01_eda.ipynb         # Exploratory analysis
│   ├── 02_preprocessing.ipynb # Data cleaning and feature engineering
│   ├── 03_modeling.ipynb    # Model training and comparison
│   └── 04_evaluation.ipynb  # Final evaluation and interpretability
├── requirements.txt         # Project dependencies
├── .gitignore               # Files and directories excluded from version control
└── README.md
```

## 3. Dataset

* **Source:** `data/raw/anemia.csv`, 1,421 records, 6 columns.
* **Raw input variables:**

| Variable     | Description                               | Unit |
| ------------ | ----------------------------------------- | ---- |
| `Gender`     | Patient's gender (0 = Male, 1 = Female)   | —    |
| `Hemoglobin` | Hemoglobin concentration                  | g/dL |
| `MCH`        | Mean corpuscular hemoglobin               | pg   |
| `MCHC`       | Mean corpuscular hemoglobin concentration | g/dL |
| `MCV`        | Mean corpuscular volume                   | fL   |

* **Target variable:** `Result` (0 = no anemia, 1 = anemia), a **binary classification** problem.
* The data was split into training, validation, and test sets, stored as NumPy arrays in `data/processed/`.

## 4. Feature Engineering (`src/preprocessing/features.py`)

Two `scikit-learn`-compatible transformers (`BaseEstimator`, `TransformerMixin`) were implemented to integrate into the inference pipeline:

### `FeatureEngineering`

Generates derived variables based on clinical domain knowledge:

* **`Low_Hb`**: binary indicator of low hemoglobin, using different thresholds according to gender (< 13 g/dL for men, < 12 g/dL for women).
* **`MCV_Cat`**: categorizes MCV as `Micro` (< 80), `Normal` (80–100), or `Macro` (> 100).
* **`HB_MCV_ratio`**: ratio between hemoglobin and MCV.
* **`MCHC_Cat`**: categorizes MCHC as `Low` (< 32), `Normal` (32–36), or `High` (> 36).
* **`MCH_Cat`**: categorizes MCH as `Low` (< 27), `Normal` (27–33), or `High` (> 33).
* **`Microcitosis`**: binary indicator derived from `MCV_Cat`.
* **`Hipocromía`**: binary indicator derived from `MCHC_Cat`.
* **`Score`**: simple hematological score, calculated as the sum of `Low_Hb` and the indicators for low MCHC, MCH, and MCV values.

### `FeatureSelector`

Receives the output array from the preprocessor and removes the columns specified in `features_to_drop`, reconstructing a DataFrame with `column_names` so that operations can be performed by column name.

According to `data/processed/feature_names.npy`, the final features used by the model are: `Gender`, `Hemoglobin`, `MCH`, `MCHC`, `MCV`, `Low_Hb`, `HB_MCV_ratio`, `Score`.

## 5. Model Selection

In `notebooks/03_modeling.ipynb`, seven algorithms were trained and compared under the same experimental conditions: `Logistic Regression` (baseline), `Decision Tree`, `Random Forest`, `XGBoost`, `LightGBM`, `CatBoost`, and `SVC`. Each model was evaluated using cross-validation and hyperparameter tuning, with **recall** prioritized as the decision metric.

**CatBoost** was selected as the final model. The serialized pipeline (`models/catboost_pipeline.pkl`) integrates the following components into a single object: feature engineering → preprocessing (encoding/scaling) → feature selection → CatBoost classifier, allowing the API to provide only the patient's raw DataFrame.

### Results on the Test Set (`notebooks/04_evaluation.ipynb`)

| Metric    | Value |
| --------- | ----- |
| Accuracy  | 0.96  |
| Precision | 0.92  |
| Recall    | 0.99  |
| F1-Score  | 0.95  |

Confusion matrix over 214 test samples: 113 true negatives, 92 true positives, 8 false positives, and **1 false negative**. The metrics remained consistent with the validation set (differences ≤ 0.02), with no relevant signs of overfitting.

### Interpretability (Feature Importance and SHAP)

`Hemoglobin` accounts for most of the model's importance, followed by `Gender` (relevant because hemoglobin reference values differ by sex) and `Low_Hb` (the derived feature created during feature engineering). SHAP values confirm that lower hemoglobin levels increase the predicted probability of anemia, while the remaining variables provide complementary information with lower relative importance.

## 6. REST API (`api/`)

Built with **FastAPI**. The trained pipeline is loaded once when the application starts (`lifespan` event) and reused for every request; the database is created automatically if it does not exist.

### Endpoints

| Method | Route               | Description                                                          |
| ------ | ------------------- | -------------------------------------------------------------------- |
| `GET`  | `/`                 | Health check.                                                        |
| `POST` | `/predict`          | Predicts anemia from patient data and saves the result.              |
| `GET`  | `/predictions/{id}` | Retrieves a stored prediction by its ID.                             |
| `GET`  | `/predictions`      | Lists all stored predictions.                                        |
| `GET`  | `/stats`            | Returns aggregated statistics (total, anemic, and non-anemic cases). |

**Security:** none of these endpoints require authentication or authorization — there are no API keys, tokens, or access controls implemented. Anyone with access to the URL can generate predictions or read the complete stored history, including measurements from other patients. The API is intended for local/development use; adding an authentication mechanism (API key, OAuth2, etc.) is a prerequisite before exposing it in a publicly accessible environment.

### `POST /predict`

**Request** (`Patient`):

```json
{
  "Gender": "Male",
  "Hemoglobin": 13.9,
  "MCH": 29.4,
  "MCHC": 33.5,
  "MCV": 88.1
}
```

Valid ranges (validated by Pydantic): `Hemoglobin` 4–20 g/dL, `MCH` 12–34 pg, `MCHC` 26–36 g/dL, `MCV` 60–120 fL.

**Response** (`PredictionResponse`):

```json
{
  "prediction": 1,
  "diagnosis": "Anemic",
  "probability": 87.69
}
```

The logic in `api/predict.py` converts gender to the numerical encoding expected by the model (0 = Male, 1 = Female), builds a single-row DataFrame, and executes `pipeline.predict` / `pipeline.predict_proba`. Any inference error is translated into an `HTTPException` 500.

### `GET /`

**Request:** receives no parameters or body.

**Response:**

```json
{
  "message": "Anemia Prediction API is running."
}
```

Simple health check with no dependency on the database or pipeline. Useful for verifying that the server is running.

### `GET /predictions/{id}`

**Request:** receives no body. It accepts a path parameter:

| Parameter | Type       | Description                               |
| --------- | ---------- | ----------------------------------------- |
| `id`      | int (path) | Identifier of the prediction to retrieve. |

Example: `GET /predictions/15`

**Response** (`PredictionRecord`), if the ID exists:

```json
{
  "id": 15,
  "gender": 1,
  "hemoglobin": 13.8,
  "mch": 29.4,
  "mchc": 33.5,
  "mcv": 88.1,
  "prediction": 1,
  "diagnosis": "Anemic",
  "probability": 97.84,
  "created_at": "2026-08-07T14:35:22Z"
}
```

If the ID does not exist in the database, it returns `404 Not Found`:

```json
{
  "detail": "Prediction not found."
}
```

### `GET /predictions`

**Request:** receives no parameters or body.

**Response:** a list of `PredictionRecord` objects, ordered by ascending `id`:

```json
[
  {
    "id": 1,
    "gender": 0,
    "hemoglobin": 15.9,
    "mch": 25.4,
    "mchc": 28.3,
    "mcv": 72.0,
    "prediction": 0,
    "diagnosis": "Not Anemic",
    "probability": 4.21,
    "created_at": "2026-08-01T10:12:03Z"
  },
  {
    "id": 2,
    "gender": 1,
    "hemoglobin": 13.8,
    "mch": 29.4,
    "mchc": 33.5,
    "mcv": 88.1,
    "prediction": 1,
    "diagnosis": "Anemic",
    "probability": 97.84,
    "created_at": "2026-08-02T09:03:41Z"
  }
]
```

If there are no predictions stored yet, it returns an empty list `[]`.

### `GET /stats`

**Request:** receives no parameters or body.

**Response** (`PredictionStats`):

```json
{
  "total_predictions": 42,
  "anemic_predictions": 18,
  "non_anemic_predictions": 24
}
```

The values are calculated at request time against the database (`database/crud.py` → `count_predictions`) and are not cached.

## 7. Persistence (`database/`)

The project uses **SQLAlchemy** with **SQLite** (`database/anemia.db`). Each prediction made through `/predict` is automatically stored in the `predictions` table, with the following columns: `id`, `gender`, `hemoglobin`, `mch`, `mchc`, `mcv`, `prediction`, `diagnosis`, `probability`, and `created_at` (automatically generated UTC timestamp).

The `database/crud.py` module exposes the following operations: `save_prediction`, `get_prediction`, `get_predictions`, and `count_predictions`, which are consumed by the `/predictions` and `/stats` endpoints.

## 8. Notebooks

| Notebook                 | Content                                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `01_eda.ipynb`           | Exploratory analysis of the raw dataset: variable distributions, relationships with the target variable, and outliers.           |
| `02_preprocessing.ipynb` | Data cleaning, design and testing of derived variables (feature engineering), and preprocessor construction.                     |
| `03_modeling.ipynb`      | Training and comparison of the seven candidate models, cross-validation, hyperparameter optimization, and final model selection. |
| `04_evaluation.ipynb`    | Final model evaluation on the test set, confusion matrix, validation vs. test comparison, Feature Importance, and SHAP.          |

## 9. Dependencies (`requirements.txt`)

| Package        | Version | Main Purpose                             |
| -------------- | ------- | ---------------------------------------- |
| `numpy`        | 2.0.2   | Numerical computing                      |
| `pandas`       | 2.2.2   | Tabular data manipulation                |
| `matplotlib`   | 3.10.0  | Visualization (notebooks)                |
| `seaborn`      | 0.13.2  | Statistical visualization (notebooks)    |
| `plotly`       | 5.24.1  | Interactive visualization (notebooks)    |
| `scipy`        | 1.16.3  | Statistical functions                    |
| `statsmodels`  | 0.14.6  | Statistical analysis (notebooks)         |
| `scikit-learn` | 1.6.1   | Pipeline, preprocessing, baseline models |
| `xgboost`      | 3.3.0   | Candidate model (comparison)             |
| `lightgbm`     | 4.6.0   | Candidate model (comparison)             |
| `joblib`       | 1.5.3   | Pipeline serialization (`api/loader.py`) |
| `shap`         | 0.52.0  | Model interpretability                   |
| `pydantic`     | 2.13.4  | API schema validation                    |
| `fastapi`      | 0.139.0 | REST API framework                       |
| `uvicorn`      | 0.51.0  | ASGI server                              |
| `SQLAlchemy`   | 2.0.51  | ORM and database access                  |

## 10. Installation and Execution

**Version requirement:** the project requires **Python 3.12** (the version used in Google Colab to train and serialize the model). `numpy==2.0.2` does not have precompiled wheels for Python 3.13; installing `requirements.txt` under that version fails when attempting to build NumPy from source (`stdalign.h not found` error with MSVC on Windows).

```bash
# Clone the repository
git clone <repository-url>
cd Anemia-Prediction-System

# Create a virtual environment with Python 3.12
py -3.12 -m venv venv
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn api.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with automatically generated interactive documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

When the application starts, it automatically creates `database/anemia.db` if it does not exist (no manual migrations are required) and loads `models/catboost_pipeline.pkl` into memory.

## 11. Version Control

The repository uses `.gitignore` to exclude files that should not be versioned: Python caches (`__pycache__/`), virtual environments, Jupyter checkpoints, type-checking caches, and local configuration files (`.env`).

Branch naming convention: `feature/<area>` for feature development (e.g., `feature/documentation`, `feature/database`) and `fix/<area>` for targeted fixes to existing code.
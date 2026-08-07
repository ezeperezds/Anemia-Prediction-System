# Anemia Prediction System

A Machine Learning system for anemia prediction based on hematological parameters, featuring a complete training pipeline, a REST API built with FastAPI, and persistent storage of prediction results.

---

## Overview

This project aims to develop a Machine Learning model capable of predicting the presence of anemia using hematological variables such as **Hemoglobin**, **MCV**, **MCH**, and **MCHC**.

Anemia is a condition characterized by a reduced number of red blood cells or insufficient hemoglobin concentration, impairing the body's ability to transport oxygen. It is considered a major global public health issue, particularly affecting children and pregnant women.

Using clinical and hematological data, several binary classification models were trained and evaluated to identify patients at risk of anemia. The project also includes a production-oriented prediction API capable of serving the trained model and storing prediction history in a relational database.

> ⚠️ **Disclaimer:** This project was developed for educational purposes as part of a Data Science portfolio. It is **not** a certified medical device and must **not** be used for clinical decision-making without the supervision of a qualified healthcare professional.

> Complete technical documentation is available in [`DOCUMENTATION.md`](./DOCUMENTATION.md).

---

# Project Structure

```
Anemia-Prediction-System/
├── api/                    # FastAPI REST API
├── database/               # SQLAlchemy models, CRUD operations and database configuration
├── src/                    # Reusable ML components (feature engineering, evaluation, etc.)
├── models/                 # Trained pipelines and serialized models
├── data/                   # Raw dataset and processed datasets
├── notebooks/              # EDA, preprocessing, modeling and model testing
├── requirements.txt
└── README.md
```

More details about the project structure are available in [`DOCUMENTATION.md`](./DOCUMENTATION.md#2-project-structure).

---

# Requirements

- **Python 3.12**

> The project was trained and serialized using Python 3.12. Some dependencies (e.g. `numpy==2.0.2`) do not provide precompiled wheels for Python 3.13, which may cause installation issues.

---

# Installation

Clone the repository and install the required dependencies.

```bash
git clone <repository-url>

cd Anemia-Prediction-System

# Create a virtual environment using Python 3.12
py -3.12 -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

# Dependencies

The project uses the following main libraries:

- FastAPI
- Pydantic
- SQLAlchemy
- Scikit-learn
- CatBoost
- XGBoost
- LightGBM
- SHAP
- Pandas
- NumPy
- Matplotlib
- Plotly

The complete dependency list is available in `requirements.txt`.

Additional details about each dependency can be found in [`DOCUMENTATION.md`](./DOCUMENTATION.md#9-dependencies-requirementstxt).

---

# REST API

The trained model is exposed through a **FastAPI** REST service.

The API receives hematological measurements from a patient, performs all preprocessing internally through the trained pipeline, returns the predicted diagnosis, and automatically stores every successful prediction in a SQLite database.

Start the server with:

```bash
uvicorn api.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive documentation:

```
http://127.0.0.1:8000/docs
```

---

## Available Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Health check |
| POST | `/predict` | Predict anemia from patient data |
| GET | `/predictions/{id}` | Retrieve a prediction by ID |
| GET | `/predictions` | Retrieve all stored predictions |
| GET | `/stats` | Retrieve aggregated prediction statistics |

Every successful prediction performed through `/predict` is automatically stored in the SQLite database.

This allows clients not only to obtain predictions, but also to:

- Retrieve previous predictions
- Query prediction history
- Obtain aggregated statistics without maintaining their own records

### Security Note

The current implementation does **not** include authentication or authorization.

It is intended for local development and educational purposes. If deployed publicly, authentication and proper access control should be implemented before production use.

---

## Example Request

### POST `/predict`

Request

```json
{
    "Gender": "Male",
    "Hemoglobin": 13.9,
    "MCH": 29.4,
    "MCHC": 33.5,
    "MCV": 88.1
}
```

Response

```json
{
    "prediction": 1,
    "diagnosis": "Anemic",
    "probability": 87.69
}
```

Complete API examples, including error responses, are available in [`DOCUMENTATION.md`](./DOCUMENTATION.md#6-rest-api-api).

---

# Machine Learning Model

Seven binary classification algorithms were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost
- LightGBM
- CatBoost
- Support Vector Machine (SVC)

Since the project addresses a medical classification problem, **Recall** was selected as the primary optimization metric to minimize false negatives.

The final model is **CatBoost**, deployed as part of a single end-to-end pipeline that performs:

```
Feature Engineering
        ↓
Preprocessing
        ↓
Feature Selection
        ↓
CatBoost Classifier
```

This architecture allows the API to receive raw patient data while all preprocessing is executed automatically inside the pipeline.

---

## Test Performance

| Metric | Score |
|---------|------:|
| Accuracy | 0.96 |
| Precision | 0.92 |
| Recall | 0.99 |
| F1-score | 0.95 |

Feature Engineering, model comparison, Feature Importance analysis, and SHAP explainability are documented in the project notebooks and the technical documentation.

---

# Technologies

- Python
- Scikit-learn
- CatBoost
- FastAPI
- SQLAlchemy
- SQLite
- SHAP
- Pandas
- NumPy
- Matplotlib
- Plotly

---

# Author

**Ezequiel Alejandro Pérez**

GitHub: https://github.com/ezeperezds

Email: ezep5993@gmail.com
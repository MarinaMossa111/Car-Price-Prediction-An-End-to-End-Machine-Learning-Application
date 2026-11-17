# 🚗 Car Price Prediction API

## 📌 Overview

The Car Price Prediction API is a RESTful backend service built with **FastAPI** that predicts the selling price of a used car using multiple machine learning models.

The API receives a car's specifications (brand, age, mileage, fuel type, transmission, and more), engineers two additional features, performs inference with the selected trained pipeline, and returns the predicted selling price along with the model used.

---

## 🚀 Features

- RESTful API built with FastAPI
- Seven machine learning models
  - Linear Regression
  - Decision Tree
  - Random Forest
  - Gradient Boosting
  - XGBoost
  - CatBoost
  - Optimized CatBoost (default)
- Automatic input validation using Pydantic
- Preprocessing (imputation, scaling, one-hot encoding) baked into each model pipeline — no manual preprocessing step in the backend
- Automatic reversal of the log-transformed target, so predictions are returned as real currency values
- Prediction history logged to SQLite
- Interactive Swagger API documentation
- Automatic OpenAPI specification
- Model serialization with Joblib
- Clean and modular project structure

---

## 🛠️ Technologies Used

- Python
- FastAPI
- Pydantic
- Scikit-learn
- XGBoost
- CatBoost
- NumPy
- Pandas
- Joblib
- Uvicorn
- SQLite

---

## 📂 Project Structure

```text
backend/
│
├── main.py
├── database.py
├── requirements.txt
└── README.md

models/
├── linear_regression.pkl
├── decision_tree.pkl
├── random_forest.pkl
├── gradient_boosting.pkl
├── xgboost.pkl
├── catboost.pkl
├── optimized_catboost.pkl
└── model_results.json

database/
├── schema.sql
└── car_price.db
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Car-Price-Prediction-with-Machine-Learning
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

**Note:** the model files in this project were trained with `scikit-learn==1.6.1`. Installing a newer scikit-learn version (e.g. 1.7.x) can break unpickling of the saved pipelines with an `AttributeError` on internal `ColumnTransformer` classes. Keep the pinned version in `requirements.txt` unless the models are retrained and re-saved.

---

## ▶️ Run the API

From inside `backend/`:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```
http://127.0.0.1:8000/redoc
```

---

## 📌 API Endpoints

### GET /

Returns API information.

Example response:

```json
{
  "message": "Welcome to the Car Price Prediction API!",
  "available_models": [
    "Linear Regression",
    "Decision Tree",
    "Random Forest",
    "Gradient Boosting",
    "XGBoost",
    "CatBoost",
    "Optimized CatBoost"
  ],
  "endpoints": {
    "prediction": "/predict",
    "models_info": "/models",
    "latest_prediction": "/latest_prediction"
  }
}
```

---

### POST /predict

Predicts the car's selling price.

Example request:

```json
{
  "algorithm": "optimized_catboost",
  "car_name": "Maruti Alto",
  "brand": "Maruti",
  "car_model": "Alto",
  "vehicle_age": 9,
  "km_driven": 120000,
  "seller_type": "Individual",
  "fuel_type": "Petrol",
  "transmission_type": "Manual",
  "mileage": 19.7,
  "engine": 796,
  "max_power": 46.3,
  "seats": 5
}
```

Example response:

```json
{
  "selected_model": "Optimized CatBoost",
  "predicted_price": 169395.94
}
```

**Note on the underlying math:** the models were trained on `log_selling_price` (a `np.log1p` transform of the raw price), not raw price directly. The `/predict` endpoint automatically reverses this with `np.expm1()` before responding, so the `predicted_price` field is always a real, human-readable currency value — no manual conversion needed by the client.

---

### GET /models

Returns the list of available models.

Example response:

```json
{
  "models": [
    "Linear Regression",
    "Decision Tree",
    "Random Forest",
    "Gradient Boosting",
    "XGBoost",
    "CatBoost",
    "Optimized CatBoost"
  ]
}
```

---

### GET /latest_prediction

Returns the most recent prediction saved to the database.

Example response:

```json
{
  "id": 1,
  "car_name": "Maruti Alto",
  "brand": "Maruti",
  "model": "Alto",
  "vehicle_age": 9,
  "km_driven": 120000,
  "seller_type": "Individual",
  "fuel_type": "Petrol",
  "transmission_type": "Manual",
  "mileage": 19.7,
  "engine": 796,
  "max_power": 46.3,
  "seats": 5,
  "predicted_price": 169395.94,
  "model_used": "Optimized CatBoost",
  "created_at": "2026-07-28 10:49:29"
}
```

---

## 🤖 Available Models

| Model | Description |
|--------|-------------|
| Linear Regression | Linear baseline regression model |
| Decision Tree | Tree-based regression model |
| Random Forest | Ensemble of decision trees |
| Gradient Boosting | Sequential ensemble that corrects prior errors |
| XGBoost | Regularized, optimized gradient boosting |
| CatBoost | Gradient boosting with native categorical support |
| Optimized CatBoost | Hyperparameter-tuned CatBoost (default, best-performing) |

See `models/README.md` for full evaluation metrics (MAE, RMSE, R²) for each model.

---

## 📊 Prediction Workflow

1. Receive user input (raw car specifications).
2. Validate request data with Pydantic.
3. Compute engineered features: `km_per_year` and `log_km_driven`.
4. Select the requested model pipeline.
5. Run `.predict()` — preprocessing (imputation, scaling, encoding) happens automatically inside the pipeline.
6. Reverse the log transform (`np.expm1`) to get the real selling price.
7. Save the input, prediction, and model used to the SQLite database.
8. Return the prediction and selected model name.

---

## 📖 Interactive API Documentation

FastAPI automatically generates interactive documentation.

- Swagger UI: `/docs`
- ReDoc: `/redoc`

These interfaces allow testing all endpoints directly from the browser without additional tools.

---

## 📄 License

This project was developed for educational and portfolio purposes. 
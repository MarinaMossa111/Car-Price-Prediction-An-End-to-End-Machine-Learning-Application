# 🚗 Car Price Prediction: An End-to-End Machine Learning Application

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![XGBoost](https://img.shields.io/badge/XGBoost-Regression-red)
![CatBoost](https://img.shields.io/badge/CatBoost-Regression-yellow)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?logo=html5)
![JavaScript](https://img.shields.io/badge/JavaScript-Interactive-F7DF1E?logo=javascript)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

## 📖 Project Overview

This project implements a complete end-to-end Machine Learning application for predicting the **selling price of a used car** based on its specifications.

Rather than focusing solely on model training, the project implements the full ML lifecycle:

- Data cleaning and feature engineering
- Training and comparing seven regression algorithms
- Model evaluation
- Saving trained models (as full preprocessing + regression pipelines)
- Deploying models using FastAPI
- Building a custom, dashboard-styled frontend interface
- Connecting frontend and backend for real-time predictions
- Storing prediction history in SQLite

Users enter a car's specifications (brand, age, mileage, fuel type, transmission, and more), select a Machine Learning model, and receive a predicted selling price through a web interface.

---

## 🎯 Project Objectives

- Build and compare multiple regression algorithms on the same dataset.
- Understand the complete ML workflow from training to deployment.
- Deploy trained models through a REST API.
- Create an interactive, custom-designed interface for real-time predictions.
- Demonstrate communication between frontend, backend, and ML models.
- Correctly handle a log-transformed target end-to-end, so the deployed API returns real, human-readable prices.

---

## ✨ Key Features

- 🚗 Used car selling price prediction
- 🤖 Seven trained regression models, dynamically selectable
- 📊 Model evaluation and comparison (MAE, RMSE, R²)
- ⚡ FastAPI REST API
- 📄 Automatic Swagger API documentation
- 🎨 Custom automotive-dashboard frontend (not a generic form)
- 🗄 SQLite database for prediction history
- 🔄 Real-time prediction responses
- 📱 Mobile-friendly, responsive interface
- 🧩 Modular project structure
- 🧮 Automatic reversal of the log-transformed target
- 🚀 Easy local deployment

---

## 🏗️ System Architecture

```text
                                User
                                  │
                                  ▼
                  ┌────────────────────────────────┐
                  │        Web Frontend            │
                  │ HTML • CSS • JavaScript         │
                  └───────────────┬────────────────┘
                                  │
                         HTTP POST Request
                                  │
                                  ▼
                  ┌────────────────────────────────┐
                  │        FastAPI Backend         │
                  │  Request Validation & Routing  │
                  └───────────────┬────────────────┘
                                  │
                 Loads Selected Machine Learning Pipeline
                                  │
                                  ▼
          ┌──────────────────────────────────────────────┐
          │       Machine Learning Pipelines              │
          │  (Preprocessor + Regressor, bundled together) │
          │                                                │
          │  • Linear Regression      • XGBoost            │
          │  • Decision Tree          • CatBoost            │
          │  • Random Forest          • Optimized CatBoost  │
          │  • Gradient Boosting                            │
          └───────────────┬────────────────────────────────┘
                                  │
                    Predict Log Selling Price
                                  │
                     Reverse Log Transform (expm1)
                                  │
                                  ▼
                  ┌────────────────────────────────┐
                  │       SQLite Database          │
                  │     Store Prediction History   │
                  └───────────────┬────────────────┘
                                  │
                           JSON API Response
                                  │
                                  ▼
                  ┌────────────────────────────────┐
                  │      Display Predicted Price   │
                  │        (Gauge Visualization)   │
                  └────────────────────────────────┘
```

---

## 🔄 Application Workflow

1. The user opens the web application.
2. The user selects one of the seven trained regression models.
3. The user enters the car's specifications (name, brand, model, age, km driven, seller type, fuel type, transmission, mileage, engine, max power, seats).
4. JavaScript validates the user input.
5. The frontend sends an HTTP POST request to the FastAPI backend.
6. FastAPI validates the incoming request using Pydantic.
7. The backend computes two engineered features (`km_per_year`, `log_km_driven`).
8. The backend loads the selected pipeline and calls `.predict()` — preprocessing happens internally.
9. The backend reverses the log transform (`np.expm1`) to produce a real price.
10. The prediction, input values, and model used are stored in the SQLite database.
11. The backend returns the prediction as a JSON response.
12. The frontend displays the price on a gauge, instantly, without refreshing the page.

---

## 📁 Project Structure

```text
Car-Price-Prediction-with-Machine-Learning/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── README.md
│
├── models/
│   ├── linear_regression.pkl
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── gradient_boosting.pkl
│   ├── xgboost.pkl
│   ├── catboost.pkl
│   ├── optimized_catboost.pkl
│   ├── model_results.json
│   └── README.md
│
├── database/
│   ├── schema.sql
│   └── car_price.db
│
├── notebook/
│   ├── Car Price Prediction.ipynb
│   └── README.md
│
├── assests/
│   ├── frontend.png
│   ├── resultsFrontend.png
│   ├── main_swagger.png
│   └── results_swagger.png
│
├── README.md
├── Documentation.md
└── LICENSE
```

---

## 📊 Dataset

The project uses a used-car listings dataset (CarDekho), containing real-world listings with specifications and sale prices.

### Features

| Feature | Description |
|---|---|
| car_name | Full car name/listing title |
| brand | Manufacturer |
| model | Specific model name |
| vehicle_age | Age of the car in years |
| km_driven | Total kilometers driven |
| seller_type | Individual, Dealer, or Trustmark Dealer |
| fuel_type | Petrol, Diesel, CNG, LPG, or Electric |
| transmission_type | Manual or Automatic |
| mileage | Fuel efficiency (kmpl) |
| engine | Engine displacement (cc) |
| max_power | Maximum power output (bhp) |
| seats | Number of seats |

### Target Variable

```
selling_price   → raw target (currency)
log_selling_price → np.log1p(selling_price), the ACTUAL target used for training
```

**This is the single most important detail in this project's ML pipeline.** Every model was trained against `log_selling_price`, not raw price. Any code that loads these models must reverse this transform (`np.expm1`) before the output is meaningful. This is documented again in the Backend and Models sections below because it's easy to forget and produces silently wrong (but not obviously broken) results if missed.

---

## ⚙️ Machine Learning Pipeline

### 1. Data Preparation

- Load and clean the dataset (handle nulls, remove duplicates, normalize inconsistent categorical text).
- Separate features (`X`) and target (`y = log_selling_price`).
- Split into training and testing sets.

### 2. Feature Engineering

Two features were engineered beyond the raw dataset columns:

- **`km_per_year`** = `km_driven / vehicle_age`
- **`log_km_driven`** = `np.log1p(km_driven)`

Both are computed before being passed into the pipeline, and both must be recomputed identically at inference time — this is handled in `backend/main.py`.

### 3. Preprocessing Pipeline

Rather than manually scaling/encoding data before training, preprocessing was built into a `ColumnTransformer` and bundled with each model inside a single `sklearn.pipeline.Pipeline`:

```python
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])
```

**Numerical features:** `vehicle_age, km_driven, mileage, engine, max_power, seats, km_per_year, log_km_driven`

**Categorical features:** `car_name, brand, model, seller_type, fuel_type, transmission_type`

Because the preprocessor lives inside the pipeline, the backend can call `pipeline.predict(raw_dataframe)` directly — no separate scaler/encoder files need to be loaded, unlike a more manual setup.

### 4. Model Training

Seven regression models were trained on the same preprocessed features:

| Model | Description |
|---------|-------------|
| Linear Regression | Linear baseline regressor |
| Decision Tree | Tree-based regressor |
| Random Forest | Ensemble of decision trees |
| Gradient Boosting | Sequential ensemble, corrects prior errors |
| XGBoost | Regularized, optimized gradient boosting |
| CatBoost | Gradient boosting with native categorical support |
| Optimized CatBoost | Hyperparameter-tuned CatBoost |

---

## 📈 Model Evaluation

Models were evaluated on the held-out test set using:

- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score**

**Important:** these metrics were computed on the `log_selling_price` scale, not raw rupees — a lower MAE/RMSE here means a better fit on the log scale the model was actually optimized against, but isn't directly interpretable as "average rupee error."

### Results

| Model | MAE | RMSE | R² Score |
|---|---:|---:|---:|
| **Optimized CatBoost** | **0.1210** | **0.1634** | **94.52%** |
| CatBoost | 0.1220 | 0.1645 | 94.45% |
| XGBoost | 0.1266 | 0.1706 | 94.02% |
| Random Forest | 0.1291 | 0.1773 | 93.55% |
| Linear Regression | 0.1409 | 0.1887 | 92.69% |
| Gradient Boosting | 0.1426 | 0.1909 | 92.52% |
| Decision Tree | 0.1644 | 0.2261 | 89.51% |

### Performance Analysis

- **Optimized CatBoost** is the best-performing model across all three metrics, and is set as the default in the API.
- The gap between **CatBoost** and **Optimized CatBoost** is small, indicating the base CatBoost configuration was already close to optimal — hyperparameter tuning provided a modest but real improvement.
- **Boosting-based models** (CatBoost, XGBoost, Gradient Boosting) outperform the single **Decision Tree**, consistent with the general expectation that ensembles reduce variance and improve generalization.
- **Linear Regression** performs respectably (92.69% R²) despite being the simplest model, suggesting the log-transformed relationship between features and price is largely well-behaved and not heavily non-linear.

### Model Selection

Rather than deploying a single model, the application allows users to select from all seven trained models through the web interface, enabling direct comparison of predictions across algorithms for the same input.

---

## 💾 Model Serialization

Each trained pipeline (preprocessing + regressor bundled together) was serialized using Joblib:

```python
import os
import joblib

os.makedirs("saved_models", exist_ok=True)

for name, model in trained_models.items():
    joblib.dump(model, f"saved_models/{name}.pkl")
```

**Compatibility note:** these `.pkl` files were created using `scikit-learn==1.6.1`. Loading them with a newer scikit-learn version (e.g. 1.7.x) can raise an `AttributeError` related to internal `ColumnTransformer` classes (`_RemainderColsList`), since pickled objects reference specific internal class implementations that can change between minor versions. The project's `requirements.txt` pins `scikit-learn==1.6.1` for this reason.

---

## ⚡ FastAPI Backend

### Backend Responsibilities

- Loading all seven trained pipelines at application startup
- Validating incoming requests using Pydantic
- Computing engineered features (`km_per_year`, `log_km_driven`) from raw user input
- Running the selected pipeline's `.predict()` method
- Reversing the log transform (`np.expm1`) to produce a real price
- Saving prediction history into SQLite
- Returning structured JSON responses
- Providing interactive API documentation through Swagger UI

### Backend Components

| Component | Purpose |
|-----------|---------|
| `main.py` | FastAPI application and API endpoints |
| `database.py` | Database creation and prediction history management |
| `models/` | Serialized ML pipelines |
| `requirements.txt` | Python dependencies |

### Request Validation

| Field | Type | Description |
|--------|------|-------------|
| algorithm | Enum | Selected regression model |
| car_name | string | Full car listing name |
| brand | string | Manufacturer |
| car_model | string | Specific model |
| vehicle_age | int | Age in years |
| km_driven | int | Total kilometers driven |
| seller_type | string | Individual / Dealer / Trustmark Dealer |
| fuel_type | string | Petrol / Diesel / CNG / LPG / Electric |
| transmission_type | string | Manual / Automatic |
| mileage | float | Fuel efficiency (kmpl) |
| engine | int | Engine displacement (cc) |
| max_power | float | Max power (bhp) |
| seats | int | Number of seats |

### API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Returns API information and available endpoints |
| GET | `/models` | Returns the list of available regression models |
| POST | `/predict` | Predicts the car's selling price |
| GET | `/latest_prediction` | Retrieves the most recent prediction stored in the database |

### Prediction Pipeline

```text
Receive Request
       │
       ▼
Validate Input (Pydantic)
       │
       ▼
Select Machine Learning Pipeline
       │
       ▼
Compute Engineered Features
(km_per_year, log_km_driven)
       │
       ▼
Predict Log Selling Price
       │
       ▼
Reverse Log Transform (np.expm1)
       │
       ▼
Save Prediction to SQLite
       │
       ▼
Return JSON Response
```

### Example Request / Response

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

```json
{
  "selected_model": "Optimized CatBoost",
  "predicted_price": 169395.94
}
```

---

## 🗄 Database Integration

The application uses SQLite for prediction history, chosen for its zero-configuration, serverless, portable nature — ideal for a project of this scale.

### Stored Fields

| Field | Description |
|--------|-------------|
| car_name, brand, model | Identifying details of the car |
| vehicle_age, km_driven | Usage details |
| seller_type, fuel_type, transmission_type | Categorical specs |
| mileage, engine, max_power, seats | Numerical specs |
| predicted_price | The model's output (in real currency, after log reversal) |
| model_used | Which of the seven models generated this prediction |
| created_at | Timestamp |

### Important Operational Note

`database.py` uses `CREATE TABLE IF NOT EXISTS`, meaning changing the schema **does not automatically apply** to an existing `.db` file. If the table structure changes (columns added/renamed), the existing `car_price.db` file must be deleted so it gets recreated fresh on the next server start. This was encountered directly during development — an early test run hit `sqlite3.OperationalError: table predictions has no column named car_name` because a stale db file (from before the schema was finalized) was still present.

---

## 🎨 Frontend

### Design Approach

Unlike a generic Tailwind form layout, the frontend uses a custom automotive-dashboard visual identity:

- **Palette:** graphite background, off-white text, amber accent (evoking an instrument cluster)
- **Typography:** Oswald (display/labels) + Inter (body/inputs)
- **Signature element:** the predicted price is displayed on an SVG speedometer-style gauge rather than plain text, tying the visualization directly to the subject matter

### Frontend Features

- Spec-sheet style input grouping (12 fields: identity, usage, categorical specs, numerical specs)
- Dropdowns for fixed-category fields (seller type, fuel type, transmission) to avoid typos that would silently zero out a one-hot encoded feature
- Real-time gauge fill based on the predicted price relative to a configurable reference maximum
- `localStorage` persistence of the latest prediction across page reloads

### Frontend Workflow

```text
Open Application
        │
        ▼
Select Machine Learning Model
        │
        ▼
Enter Car Specifications
        │
        ▼
Send HTTP POST Request
        │
        ▼
Receive JSON Response
        │
        ▼
Display Predicted Price + Gauge Fill
        │
        ▼
Display Selected Model
```

---

## 🚀 Installation & Setup

### Prerequisites

| Software | Recommended Version |
|-----------|---------------------|
| Python | 3.10 or later |
| Git | Latest Version |
| Visual Studio Code | Latest Version |
| Live Server Extension (VS Code) | Latest Version |
| Web Browser | Chrome, Edge, or Firefox |

### Setup Steps

```bash
git clone https://github.com/<your-username>/car-price-prediction.git
cd car-price-prediction

python -m venv venv
venv\Scripts\activate

cd backend
pip install -r requirements.txt

uvicorn main:app --reload
```

Open the frontend:

```
frontend/index.html
```

via Live Server, typically at `http://127.0.0.1:5500`.

---

## 🛠 Troubleshooting

### `AttributeError: Can't get attribute '_RemainderColsList'`

This means scikit-learn's installed version doesn't match the version the models were trained/pickled with. Fix:

```bash
pip install scikit-learn==1.6.1
```

### `sqlite3.OperationalError: table predictions has no column named ...`

A stale `.db` file exists from before the schema was finalized. Delete `database/car_price.db` and restart the server — it will be recreated automatically with the current schema.

### Predicted price looks wildly wrong (e.g. `12.04` instead of a real price)

This means the log-price reversal (`np.expm1`) is missing from `main.py`. The models output `log_selling_price`, not raw price — the reversal step is mandatory, not optional.

### Backend fails to start / `ModuleNotFoundError`

Ensure the virtual environment is activated and dependencies are installed:

```bash
cd backend
pip install -r requirements.txt
```

### Frontend cannot connect to the backend

Verify that:
- The FastAPI server is running.
- The backend URL in `script.js` matches where uvicorn is actually running.
- CORS origins in `main.py` include the frontend's actual address.

---

## 🔮 Future Improvements

- Add a full prediction history view in the frontend (not just the latest one).
- Store model evaluation metrics dynamically rather than in a static table.
- Add Docker support for consistent environment reproduction.
- Migrate to PostgreSQL for larger-scale deployments.
- Add a CI/CD pipeline (GitHub Actions).
- Deploy to a cloud platform (Render, Railway, Azure).
- Make the gauge's reference maximum dynamic, based on live dataset statistics.
- Add automated tests covering the log-price reversal logic specifically, since it's the easiest part of this pipeline to silently break.

---

## 🧪 Testing

The application has been manually tested across the following scenarios:

- Valid prediction requests across all seven models
- Schema/database mismatches after a schema change (and the fix, documented above)
- scikit-learn version mismatch on model loading (and the fix, documented above)
- Log-price reversal correctness (verified against expected real-world price ranges)
- Swagger UI request/response validation
- Frontend-to-backend CORS communication

---

## 📜 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this project under the terms of the MIT License. See the `LICENSE` file for details.

---

## 👨‍💻 Author

**[Your Name]**

Computer Science & Artificial Intelligence Graduate

Passionate about Machine Learning, backend development, and full-stack AI applications.

---

## 📚 References

- CarDekho Used Car Dataset (Kaggle)
- Scikit-learn Documentation
- XGBoost Documentation
- CatBoost Documentation
- FastAPI Documentation
- Pandas / NumPy Documentation
- SQLite Documentation

---

## 📬 Contact

- LinkedIn: https://linkedin.com/in/your-profile
- GitHub: https://github.com/your-username
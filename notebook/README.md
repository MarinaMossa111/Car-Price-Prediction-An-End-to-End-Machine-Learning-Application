# 🚗 Car Price Prediction: Machine Learning Models

---

## 📌 Project Overview

This folder contains the trained Machine Learning models and preprocessing pipeline used in the Car Price Prediction project.

The models were trained to predict the **selling price of a used car** based on its specifications:

- Car Name, Brand, Model
- Vehicle Age
- Kilometers Driven
- Seller Type
- Fuel Type
- Transmission Type
- Mileage
- Engine (cc)
- Max Power (bhp)
- Seats

This folder contains the serialized models that are loaded by the FastAPI backend to perform real-time price predictions.

---

# 📂 Models Directory Structure

```

models/

│
├── linear_regression.pkl
├── decision_tree.pkl
├── random_forest.pkl
├── gradient_boosting.pkl
├── xgboost.pkl
├── catboost.pkl
├── optimized_catboost.pkl
│
└── model_results.json

```

**Note:** unlike a typical scikit-learn setup with separate scaler/encoder files, every `.pkl` file above is a complete **sklearn Pipeline** — preprocessing and regressor bundled together. There are no standalone `scaler.pkl` or `encoder.pkl` files, because preprocessing is baked into each model file itself.

---

# 🤖 Trained Machine Learning Models

The following regression algorithms were trained and saved:

---

## Linear Regression

A baseline linear model that estimates selling price as a weighted combination of input features.

File:

```

linear_regression.pkl

```

---

## Decision Tree

A tree-based model that learns price-splitting rules from the training data.

File:

```

decision_tree.pkl

```

---

## Random Forest

An ensemble of decision trees that averages predictions to reduce overfitting and improve accuracy.

File:

```

random_forest.pkl

```

---

## Gradient Boosting

A sequential ensemble method where each tree corrects the errors of the previous ones.

File:

```

gradient_boosting.pkl

```

---

## XGBoost

An optimized, regularized implementation of gradient boosting, tuned for speed and performance.

File:

```

xgboost.pkl

```

---

## CatBoost

A gradient boosting algorithm with native, efficient handling of categorical features.

File:

```

catboost.pkl

```

---

## Optimized CatBoost

A hyperparameter-tuned version of CatBoost, selected as the best-performing model.

File:

```

optimized_catboost.pkl

```

---

# ⚙️ Preprocessing Pipeline

Each saved model is a full `sklearn.pipeline.Pipeline` containing two stages:

```python
Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', <model>)
])
```

Where `preprocessor` is a `ColumnTransformer`:

```python
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])
```

**Numerical features** (imputed with median, then scaled):

```
vehicle_age, km_driven, mileage, engine, max_power,
seats, km_per_year, log_km_driven
```

**Categorical features** (imputed with most frequent, then one-hot encoded):

```
car_name, brand, model, seller_type, fuel_type, transmission_type
```

**Engineered features** — computed before being passed into the pipeline, not present in the raw dataset:

- `km_per_year` = `km_driven / vehicle_age`
- `log_km_driven` = `log1p(km_driven)`

Because preprocessing lives inside each pipeline, the FastAPI backend can call `.predict()` directly on raw input — no manual scaling or encoding step is needed outside of computing the two engineered features above.

---

# 🎯 Target Variable

**Important:** these models were **not** trained on raw `selling_price`. They were trained on a log-transformed target:

```python
y = df['log_selling_price']   # = np.log1p(selling_price)
```

This means every prediction returned by `.predict()` is a **log-price**, not a real currency value. The backend must reverse this transform before the result means anything:

```python
predicted_price = np.expm1(model.predict(input_data)[0])
```

This is handled in `backend/main.py`. If you retrain or add a new model in the future, make sure it's trained the same way (on `log_selling_price`) — otherwise the reversal step in `main.py` will silently produce a wrong result rather than an error.

---

# 📊 Model Evaluation Results

The trained models were evaluated using:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score

Evaluation results are stored in:

```

model_results.json

```

**Note:** since the models were trained on `log_selling_price`, the MAE/RMSE values below are measured in **log-price units**, not rupees. A lower value still means a better fit, but these numbers aren't directly readable as "average rupee error" — they're on the log scale the model actually optimized against.

## Results

| Model | MAE | RMSE | R² Score |
|---|---|---|---|
| Optimized CatBoost | 0.1210 | 0.1634 | 0.9452 |
| CatBoost | 0.1220 | 0.1645 | 0.9445 |
| XGBoost | 0.1266 | 0.1706 | 0.9402 |
| Random Forest | 0.1291 | 0.1773 | 0.9355 |
| Linear Regression | 0.1409 | 0.1887 | 0.9269 |
| Gradient Boosting | 0.1426 | 0.1909 | 0.9252 |
| Decision Tree | 0.1644 | 0.2261 | 0.8951 |

**Optimized CatBoost** is the best-performing model (highest R², lowest MAE/RMSE) and is set as the default in the backend's `algorithm` selector.

---

# 💾 Model Serialization

All trained pipelines were saved using Joblib.

```python
import os
import joblib

os.makedirs("saved_models", exist_ok=True)

for name, model in trained_models.items():
    joblib.dump(model, f"saved_models/{name}.pkl")
```

These files allow the application to load fully-fitted pipelines directly, without retraining or re-fitting the preprocessor.

---

# 🔄 Prediction Workflow

```
User Input (raw car specs)

↓

Compute Engineered Features
(km_per_year, log_km_driven)

↓

Selected Pipeline
(preprocessor + regressor, bundled together)

↓

Log-Price Prediction

↓

Reverse Log Transform
(np.expm1)

↓

Real Selling Price Output
```

---

# 🔗 Backend Integration

The FastAPI backend loads all seven pipelines at startup:

```python
model = joblib.load(
    "models/optimized_catboost.pkl"
)
```

The loaded models are then used through:

```
POST /predict
```

API endpoint, with the model selectable via the `algorithm` field in the request body.

---

# 🛠️ Technologies Used

* Python
* Scikit-learn
* XGBoost
* CatBoost
* NumPy
* Pandas
* Joblib
* Jupyter Notebook

---

# 📌 Notes

* The models were trained on the CarDekho used-car dataset.
* All models share the same preprocessing pipeline structure, fit independently per model.
* Predictions are returned on a log scale internally and reversed with `np.expm1()` in the backend.
* The backend can dynamically select between all seven trained models per request.

---

# 🔮 Future Improvements

Possible improvements:

* Add cross-validation results alongside the single train/test split metrics.
* Track feature importance per model in `model_results.json`, not just accuracy metrics.
* Add model versioning as new training runs are made.
* Automate retraining pipelines when new data is available.
* Deploy models using cloud services.

---

# 👤 Author

**[MarinaMossa]**

Machine Learning Enthusiast | AI Engineer
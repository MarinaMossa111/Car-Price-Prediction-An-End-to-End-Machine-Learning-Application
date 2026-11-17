from pathlib import Path
from enum import Enum

import joblib
import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import (
    create_database,
    save_prediction,
    get_latest_prediction
)


# ======================================================
# FastAPI
# ======================================================

app = FastAPI(
    title="Car Price Prediction API",
    description="Predict used car selling prices using multiple Machine Learning models.",
    version="1.0.0",
)


# Create database
create_database()



# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ======================================================
# Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"



# ======================================================
# Load Models
# ======================================================
# NOTE: each of these is a full sklearn Pipeline
# (preprocessor + regressor baked together), so raw
# input can be passed directly to .predict().
#
# NOTE: these models were trained on log_selling_price
# (via np.log1p), NOT raw selling_price. So every
# prediction must be reversed with np.expm1() before
# it means anything in real currency.

models = {

    "linear_regression": {

        "name": "Linear Regression",

        "model": joblib.load(
            MODEL_DIR / "linear_regression.pkl"
        )

    },


    "decision_tree": {

        "name": "Decision Tree",

        "model": joblib.load(
            MODEL_DIR / "decision_tree.pkl"
        )

    },


    "random_forest": {

        "name": "Random Forest",

        "model": joblib.load(
            MODEL_DIR / "random_forest.pkl"
        )

    },


    "gradient_boosting": {

        "name": "Gradient Boosting",

        "model": joblib.load(
            MODEL_DIR / "gradient_boosting.pkl"
        )

    },


    "xgboost": {

        "name": "XGBoost",

        "model": joblib.load(
            MODEL_DIR / "xgboost.pkl"
        )

    },


    "catboost": {

        "name": "CatBoost",

        "model": joblib.load(
            MODEL_DIR / "catboost.pkl"
        )

    },


    "optimized_catboost": {

        "name": "Optimized CatBoost",

        "model": joblib.load(
            MODEL_DIR / "optimized_catboost.pkl"
        )

    }

}



# ======================================================
# Model Enum
# ======================================================

class ModelType(str, Enum):

    linear_regression = "linear_regression"

    decision_tree = "decision_tree"

    random_forest = "random_forest"

    gradient_boosting = "gradient_boosting"

    xgboost = "xgboost"

    catboost = "catboost"

    optimized_catboost = "optimized_catboost"



# ======================================================
# Request Model
# ======================================================

class CarFeatures(BaseModel):

    algorithm: ModelType = Field(
        default=ModelType.optimized_catboost
    )

    car_name: str

    brand: str

    car_model: str

    vehicle_age: int

    km_driven: int

    seller_type: str

    fuel_type: str

    transmission_type: str

    mileage: float

    engine: int

    max_power: float

    seats: int



# ======================================================
# Response Model
# ======================================================

class PredictionResponse(BaseModel):

    selected_model: str

    predicted_price: float



# ======================================================
# Home Endpoint
# ======================================================

@app.get("/")
def home():

    return {

        "message": "Welcome to the Car Price Prediction API!",

        "available_models": [

            model["name"]

            for model in models.values()

        ],

        "endpoints": {

            "prediction": "/predict",

            "models_info": "/models",

            "latest_prediction": "/latest_prediction"

        }

    }



# ======================================================
# Models Endpoint
# ======================================================

@app.get("/models")
def get_models():

    return {

        "models": [
            info["name"] for info in models.values()
        ]

    }



# ======================================================
# Prediction Endpoint
# ======================================================

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(features: CarFeatures):


    selected = models.get(
        features.algorithm.value
    )


    if selected is None:

        raise HTTPException(

            status_code=400,

            detail="Model not available"

        )



    # ===============================
    # Engineered Features
    # ===============================

    km_per_year = (

        features.km_driven / features.vehicle_age

        if features.vehicle_age > 0

        else float(features.km_driven)

    )


    log_km_driven = float(
        np.log1p(features.km_driven)
    )



    # ===============================
    # Build Input Row
    # ===============================

    input_data = pd.DataFrame([{

        "car_name": features.car_name,

        "brand": features.brand,

        "model": features.car_model,

        "vehicle_age": features.vehicle_age,

        "km_driven": features.km_driven,

        "seller_type": features.seller_type,

        "fuel_type": features.fuel_type,

        "transmission_type": features.transmission_type,

        "mileage": features.mileage,

        "engine": features.engine,

        "max_power": features.max_power,

        "seats": features.seats,

        "km_per_year": km_per_year,

        "log_km_driven": log_km_driven

    }])



    model = selected["model"]



    prediction = model.predict(
        input_data
    )



    # ===============================
    # Reverse Log Transform
    # ===============================
    # Models were trained on log_selling_price
    # (np.log1p), so we reverse it here with
    # np.expm1() to get the real price back.

    predicted_price = round(
        float(np.expm1(prediction[0])),
        2
    )



    # ===============================
    # Save Prediction To Database
    # ===============================

    save_prediction(

        features.car_name,

        features.brand,

        features.car_model,

        features.vehicle_age,

        features.km_driven,

        features.seller_type,

        features.fuel_type,

        features.transmission_type,

        features.mileage,

        features.engine,

        features.max_power,

        features.seats,

        predicted_price,

        selected["name"]

    )



    # ===============================
    # Return Result To Frontend
    # ===============================

    result = {

        "selected_model": selected["name"],

        "predicted_price": predicted_price

    }


    return result



# ======================================================
# Latest Prediction Endpoint
# ======================================================

@app.get("/latest_prediction")
def latest_prediction():


    result = get_latest_prediction()



    if result is None:

        return {

            "message": "No predictions available"

        }



    return result
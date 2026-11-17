# 🚗 Car Price Prediction - Frontend

## 📌 Overview

This is the frontend interface for the **Car Price Prediction** project.

The application provides an interactive web interface where users can:

- Select a Machine Learning model
- Enter used car specifications
- Send prediction requests to the FastAPI backend
- View the predicted selling price
- View the selected model used for the prediction

The frontend communicates with the backend API to perform real-time machine learning predictions.

---

# ✨ Features

- 🚗 Dashboard-style, distinctive user interface (not a generic form)
- 🤖 Selection across all seven trained Machine Learning models
- 📊 Predicted price displayed on a speedometer-style gauge
- 🔗 Real-time communication with FastAPI backend
- ⚡ Asynchronous API requests using JavaScript Fetch API
- 🎨 Custom styling (Oswald + Inter typefaces, graphite/amber palette) — no generic Tailwind template look

---

# 🏗️ Project Structure

```
frontend/
│
├── index.html        # Main user interface
│
├── script.js         # API communication, gauge logic, and prediction handling
│
└── README.md          # Frontend documentation
```

---

# 🖥️ Technologies Used

## HTML5

Used to create the structure of the web application, including the spec-sheet input layout and the SVG gauge.

## JavaScript (ES6)

Used for:

- Handling user input across 12 car specification fields
- Sending API requests
- Processing backend responses
- Updating the predicted price and gauge fill dynamically
- Persisting the latest prediction in `localStorage`

## CSS (custom, Tailwind-free)

Used for:

- A dark, automotive-dashboard visual identity (graphite background, amber accent)
- Responsive layout down to mobile
- The gauge/result panel styling

---

# 🔗 Backend Connection

The frontend communicates with the FastAPI backend through:

```
POST http://127.0.0.1:8000/predict
```

The frontend sends a JSON request:

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

The backend returns:

```json
{
  "selected_model": "Optimized CatBoost",
  "predicted_price": 169395.94
}
```

The frontend already receives the final, real-currency prediction — the log-price reversal happens on the backend, so no conversion is needed client-side.

---

# 🚀 Running the Frontend

## 1. Start the Backend API First

Navigate to the project's `backend/` folder:

```bash
cd Car-Price-Prediction-with-Machine-Learning/backend
```

Activate the virtual environment:

Windows:

```powershell
venv\Scripts\activate
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

---

## 2. Run the Frontend

Open the frontend folder:

```
frontend/
```

Open:

```
index.html
```

or use VS Code Live Server.

Example:

```
http://127.0.0.1:5500/frontend/index.html
```

---

# 🎯 User Workflow

1. Open the application
2. Select a Machine Learning model:

- Optimized CatBoost (default)
- CatBoost
- XGBoost
- Random Forest
- Gradient Boosting
- Decision Tree
- Linear Regression

3. Enter the car's specifications:

- Car Name, Brand, Model
- Vehicle Age, Kilometers Driven
- Seller Type, Fuel Type, Transmission Type
- Mileage, Engine, Max Power, Seats

4. Click:

```
Run Prediction
```

5. The application displays:

- Estimated selling price
- A gauge showing the price relative to a reference scale
- The model used for the prediction

---

# 📸 Application Preview

Example prediction:

```
Estimated Selling Price

💰 ₹ 1,69,396

🤖 Model:
Optimized CatBoost
```

---

# 🔐 CORS Configuration

The backend allows frontend communication using FastAPI CORS middleware.

Allowed origins:

```
http://127.0.0.1:5500
http://localhost:5500
```

---

# 🔮 Future Improvements

Possible enhancements:

- Add a model comparison view (accuracy/MAE/RMSE per model, side by side)
- Display prediction history from `/latest_prediction` (or a full history endpoint) in the UI
- Deploy frontend and backend online
- Make the gauge scale dynamic (based on live dataset stats) instead of a fixed reference max
- Add input validation feedback (e.g. warn on unrealistic mileage/engine combos)

---

# 👨‍💻 Author

Car Price Prediction is an end-to-end Machine Learning deployment project including:

- Data preprocessing and feature engineering
- Training and evaluation of seven regression models
- FastAPI backend with a dynamic model selector
- Interactive, custom-designed frontend interface
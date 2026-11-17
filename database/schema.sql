CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_name TEXT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    vehicle_age INTEGER NOT NULL,
    km_driven INTEGER NOT NULL,
    seller_type TEXT NOT NULL,
    fuel_type TEXT NOT NULL,
    transmission_type TEXT NOT NULL,
    mileage REAL NOT NULL,
    engine INTEGER NOT NULL,
    max_power REAL NOT NULL,
    seats INTEGER NOT NULL,
    predicted_price REAL NOT NULL,
    model_used TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
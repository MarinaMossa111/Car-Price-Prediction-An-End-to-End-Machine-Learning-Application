import sqlite3
from pathlib import Path


# ==============================
# Database Path
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "car_price.db"



# ==============================
# Create Database
# ==============================

def create_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        car_name TEXT NOT NULL,

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

    )
    """)


    connection.commit()

    connection.close()


    print("Database and table created successfully!")



# ==============================
# Save Prediction
# ==============================

def save_prediction(
    car_name,
    brand,
    model,
    vehicle_age,
    km_driven,
    seller_type,
    fuel_type,
    transmission_type,
    mileage,
    engine,
    max_power,
    seats,
    predicted_price,
    model_used
):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO predictions
        (
            car_name,
            brand,
            model,
            vehicle_age,
            km_driven,
            seller_type,
            fuel_type,
            transmission_type,
            mileage,
            engine,
            max_power,
            seats,
            predicted_price,
            model_used
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,
        (
            car_name,
            brand,
            model,
            vehicle_age,
            km_driven,
            seller_type,
            fuel_type,
            transmission_type,
            mileage,
            engine,
            max_power,
            seats,
            predicted_price,
            model_used
        )
    )


    connection.commit()

    connection.close()


    print("Prediction saved successfully!")



# ==============================
# Latest Prediction
# ==============================

def get_latest_prediction():


    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *

        FROM predictions

        ORDER BY id DESC

        LIMIT 1

        """
    )


    row = cursor.fetchone()


    connection.close()



    if row:


        return {

            "id": row[0],

            "car_name": row[1],

            "brand": row[2],

            "model": row[3],

            "vehicle_age": row[4],

            "km_driven": row[5],

            "seller_type": row[6],

            "fuel_type": row[7],

            "transmission_type": row[8],

            "mileage": row[9],

            "engine": row[10],

            "max_power": row[11],

            "seats": row[12],

            "predicted_price": row[13],

            "model_used": row[14],

            "created_at": row[15]

        }



    return {

        "message":"No prediction found"

    }
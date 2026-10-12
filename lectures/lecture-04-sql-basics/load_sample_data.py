
import json
import os
from pathlib import Path

import psycopg2


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"


def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "enterprise_open_data"),
        user=os.getenv("PGUSER", "eodp_user"),
        password=os.getenv("PGPASSWORD"),
    )


def load_weather(cursor):
    with open(SAMPLE_DIR / "weather_sample.json", encoding="utf-8") as file:
        data = json.load(file)

    hourly = data["hourly"]

    for i, forecast_time in enumerate(hourly["time"]):
        cursor.execute(
            """
            INSERT INTO weather.forecasts
                (city, latitude, longitude, forecast_time,
                 temperature_c, humidity_pct, precipitation_mm,
                 wind_speed_kmh)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                data["city"],
                data["latitude"],
                data["longitude"],
                forecast_time,
                hourly["temperature_2m"][i],
                hourly["relative_humidity_2m"][i],
                hourly["precipitation"][i],
                hourly["wind_speed_10m"][i],
            ),
        )


def load_currencies(cursor):
    with open(SAMPLE_DIR / "nbg_sample.json", encoding="utf-8") as file:
        data = json.load(file)

    for item in data["rates"]:
        cursor.execute(
            """
            INSERT INTO currency.currencies (code, name)
            VALUES (%s, %s)
            ON CONFLICT (code) DO NOTHING
            """,
            (item["code"], item["code"]),
        )

        cursor.execute(
            """
            INSERT INTO currency.rates
                (currency_code, quantity, rate, rate_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (currency_code, rate_date) DO NOTHING
            """,
            (item["code"], item["quantity"], item["rate"], data["date"]),
        )


def load_earthquakes(cursor):
    with open(
        SAMPLE_DIR / "earthquakes_sample.geojson", encoding="utf-8"
    ) as file:
        data = json.load(file)

    for feature in data["features"]:
        properties = feature["properties"]
        longitude, latitude = feature["geometry"]["coordinates"]

        cursor.execute(
            """
            INSERT INTO seismic.events
                (event_id, magnitude, place, event_time,
                 latitude, longitude, depth_km)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                properties["id"],
                properties["magnitude"],
                properties["place"],
                properties["time"],
                latitude,
                longitude,
                0,
            ),
        )


def main():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            load_weather(cursor)
            load_currencies(cursor)
            load_earthquakes(cursor)

    print("Sample data loaded successfully.")


if __name__ == "__main__":
    main()

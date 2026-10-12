
CREATE TABLE IF NOT EXISTS weather.forecasts (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    forecast_time TIMESTAMPTZ NOT NULL,
    temperature_c NUMERIC(5,2),
    humidity_pct NUMERIC(5,2),
    precipitation_mm NUMERIC(7,2),
    wind_speed_kmh NUMERIC(7,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS currency.currencies (
    code CHAR(3) PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS currency.rates (
    id SERIAL PRIMARY KEY,
    currency_code CHAR(3) NOT NULL
        REFERENCES currency.currencies(code),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    rate NUMERIC(10,4) NOT NULL CHECK (rate > 0),
    rate_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (currency_code, rate_date)
);

CREATE TABLE IF NOT EXISTS seismic.events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(100) NOT NULL UNIQUE,
    magnitude NUMERIC(4,2) NOT NULL,
    place VARCHAR(255),
    event_time TIMESTAMPTZ NOT NULL,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    depth_km NUMERIC(8,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

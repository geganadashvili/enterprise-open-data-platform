-- Lecture 3: Initial schemas for the three data sources.

CREATE SCHEMA IF NOT EXISTS weather;
COMMENT ON SCHEMA weather IS 'Open-Meteo API weather data for Georgia';

CREATE SCHEMA IF NOT EXISTS currency;
COMMENT ON SCHEMA currency IS 'National Bank of Georgia currency exchange-rate data';

CREATE SCHEMA IF NOT EXISTS seismic;
COMMENT ON SCHEMA seismic IS 'USGS Earthquake Catalog seismic data for the Georgia region';

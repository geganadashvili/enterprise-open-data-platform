
"""Lecture 7: Open-Meteo REST API client."""

import logging
from typing import Any, Optional

import requests

from .config import WeatherConfig, load_weather_config

logger = logging.getLogger(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherAPIError(Exception):
    """Raised when the weather API request fails."""


class WeatherClient:
    """Client for retrieving current weather from Open-Meteo."""

    def __init__(self, config: Optional[WeatherConfig] = None) -> None:
        self.config = config or load_weather_config()

    def get_current_weather(self) -> dict[str, Any]:
        """Fetch current weather data from the API."""
        params = {
            "latitude": self.config.latitude,
            "longitude": self.config.longitude,
            "current": "temperature_2m,wind_speed_10m",
            "timezone": self.config.timezone,
        }

        logger.info("Requesting current weather from Open-Meteo")

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=self.config.timeout_seconds,
            )
            response.raise_for_status()

        except requests.Timeout as exc:
            logger.error("Weather API request timed out")
            raise WeatherAPIError("The weather API request timed out.") from exc

        except requests.RequestException as exc:
            logger.error("Weather API request failed: %s", exc)
            raise WeatherAPIError(f"Weather API request failed: {exc}") from exc

        data = response.json()
        current = data.get("current", {})

        logger.info(
            "Weather retrieved: temperature=%s°C, wind_speed=%s km/h, time=%s",
            current.get("temperature_2m"),
            current.get("wind_speed_10m"),
            current.get("time"),
        )

        return data

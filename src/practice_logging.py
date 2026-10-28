
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ingestion.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)

url = "https://jsonplaceholder.typicode.com/posts"

try:
    logger.info("Starting API request")

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    database = response.json()

    logger.info("Successfully retrieved data from the API")
    logger.info("Number of posts retrieved: %s", len(database))

except requests.exceptions.Timeout:
    logger.error("Request timed out. Please try again later.")

except requests.exceptions.HTTPError:
    logger.error("HTTP error occurred: %s", response.status_code)

except requests.exceptions.RequestException:
    logger.error("A network error occurred.")

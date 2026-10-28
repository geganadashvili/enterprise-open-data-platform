import requests
import logging
import os
from dotenv import load_dotenv

url = "https://openlibrary.org/search.json"
load_dotenv()
query = os.getenv("BOOK_QUERY", "python")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ingestion.log", encoding="utf-8")
    ]
)

try:
    response = requests.get(url, params={"q": query}, timeout=10)
    response.raise_for_status()
    data = response.json()
    status = response.status_code
except requests.Timeout:
    logging.error("Request timed out. Please try again later.")
except requests.HTTPError as e:
    logging.error("HTTP error occurred: %s", e)
except requests.RequestException:
    logging.error("A network error occurred.")
else:
    total_years = 0
    count = 0

    logging.info("data type: %s", type(data))
    logging.info("Status code: %s", status)


    for book in data['docs'][:5]:
        print("title: ", book['title'], 
            "first_publish_year: ", book.get('first_publish_year', 'unknown'))

    for book in data['docs'][:20]:
        year = book.get('first_publish_year', None)
        if year is not None and isinstance(year, int):
            total_years += year
            count += 1
    if count > 0:
        avg_year = round(total_years / count,2)
        print("Average first publish year:", avg_year)
    else:
        print("No valid first publish years found.")
import requests

url ="https://httpbin.org/delay/5"

try:
    response = requests.get(url, timeout=2)
    status = response.raise_for_status()
    parse = response.json()

    print("Length: ", len (parse))

except requests.exceptions.Timeout:
    print("Request timed out. Please try again later.")
except requests.exceptions.HTTPError:
    print("HTTP error occurred:", response.status_code)
except requests.exceptions.RequestException:
    print("An error occurred:")



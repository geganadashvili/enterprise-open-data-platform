import requests

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url)
response.raise_for_status()
database = response.json()
title_length = 0

for user in (database[:]):
    title_length = title_length + len(user['title'])
    avg_length = title_length / len(database)


print (title_length)

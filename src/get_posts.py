import requests

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)
response.raise_for_status()
posts = response.json()
total_title_length = 0

for length in (posts[:]):
    title_length = len (length['title'])
    total_title_length = total_title_length + title_length
    avg_length = total_title_length /len(posts)

print("Total length of all titles:", total_title_length)
print("N of posts:", len(posts))
print("Average title length:", avg_length)
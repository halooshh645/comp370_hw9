import json, requests

url = "https://arctic-shift.photon-reddit.com/api/posts/search"
params = {"subreddit": "concordia", "limit": 100, "sort": "desc"}
with open("concordia.json", "w") as f:
    json.dump(requests.get(url, params = params).json(), f)

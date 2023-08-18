import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAAG5ZowEAAAAAJz4E4Pchk022%2FuSHrucuriOVASc%3DRpiEC2Hl0vdSUKd3djkygrXsaVpXCok8tHtZzs2gJxZezoZlDd"

# Set the API endpoint URL
url = "https://api.twitter.com/2/tweets/recent"

# Set the request headers
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

# Set the request parameters
params = {
    "query": "python",
    "max_results": 10
}

# Send the GET request to the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Extract the JSON data from the response
    data = response.json()

    # Process the data
    for tweet in data.get("data", []):
        tweet_id = tweet.get("id")
        tweet_text = tweet.get("text")
        print(f"Tweet ID: {tweet_id}\nTweet Text: {tweet_text}")
else:
    # Handle request error
    print(f"Request error: {response.status_code} - {response.text}")
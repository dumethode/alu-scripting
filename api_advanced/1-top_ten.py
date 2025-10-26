#!/usr/bin/python3
import requests

def top_ten(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {'User-Agent': 'MethodeBot/0.1'}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            print(None)
            return

        data = response.json().get('data', {}).get('children', [])
        if not data:
            print(None)
            return

        for post in data:
            print(post['data']['title'])

    except Exception:
        print(None)


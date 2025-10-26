#!/usr/bin/python3
"""
Module that queries the Reddit API and prints the titles of the first
10 hot posts for a given subreddit
"""
import requests


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    for a given subreddit.

    Args:
        subreddit: name of the subreddit

    Returns:
        None (prints titles or None if invalid)
    """
    if subreddit is None or not isinstance(subreddit, str):
        print("None")
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'MyRedditScript/1.0'
    }
    params = {'limit': 10}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=5)
        if response.status_code == 200:
            data = response.json()
            children = data.get('data', {}).get('children', [])
            if not children:
                print("None")
                return
            for post in children:
                print(post.get('data', {}).get('title'))
        else:
            print("None")
    except Exception:
        print("None")

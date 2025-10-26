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
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    params = {'limit': 10}

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            for post in posts:
                title = post.get('data', {}).get('title')
                print(title)
        else:
            print(None)
    except Exception:
        print(None)

#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts
for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """
    Prints the titles of the 10 hottest posts for a subreddit.
    Prints None if the subreddit is invalid.
    """
    # Define the API endpoint for hot posts, limit to 10
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {
        'User-Agent': 'alx-project-advanced-api:v1.0.0 (by /u/dumethode)'
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code == 200:
            data = response.json()
            # Extract the list of posts
            posts = data['data']['children']

            # Print the title of each post
            for post in posts:
                print(post['data']['title'])
        else:
            # Print None for invalid subreddits
            print("None")

    except requests.exceptions.RequestException:
        print("None")

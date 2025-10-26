#!/usr/bin/python3
"""
Queries the Reddit API and returns the number of subscribers
for a given subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    Returns 0 if the subreddit is invalid.
    """
    # Define the required custom User-Agent and API endpoint
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {
        'User-Agent': 'alx-project-advanced-api:v1.0.0 (by /u/dumethode)'
    }

    try:
        # Send GET request. allow_redirects=False is required.
        response = requests.get(url, headers=headers, allow_redirects=False)

        # Check if the status code indicates a successful request (200 OK)
        if response.status_code == 200:
            data = response.json()
            # Extract the 'subscribers' field from the response data
            return data['data']['subscribers']
        else:
            # Return 0 for invalid subreddits (404 Not Found) or other errors
            return 0

    except requests.exceptions.RequestException:
        # Handle connection errors
        return 0

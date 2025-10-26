#!/usr/bin/python3
"""
Recursively queries the Reddit API to get all hot articles
for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Returns a list of titles of all hot articles for a given subreddit.
    Returns None if the subreddit is invalid.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'alx-project-advanced-api:v1.0.0 (by /u/dumethode)'
    }
    
    # Set up parameters for pagination
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        if response.status_code != 200:
            # Return None if the subreddit is invalid (base case)
            return None

        data = response.json().get("data")
        children = data.get("children")
        
        # Base case: No more posts
        if not children:
            # If it's the first call and no posts, return None
            if not hot_list:
                return None
            return hot_list

        # Recursive step: Add titles and call again with the new 'after' value
        for post in children:
            hot_list.append(post.get("data").get("title"))

        next_after = data.get("after")

        if next_after is not None:
            # Recursive call with the next page's 'after' token
            return recurse(subreddit, hot_list, next_after)
        
        # Final base case: 'after' is None, meaning we have reached the end
        return hot_list

    except requests.exceptions.RequestException:
        return None

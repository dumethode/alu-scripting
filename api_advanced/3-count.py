#!/usr/bin/python3
"""
Recursively queries the Reddit API, counts keywords in all hot article titles,
and prints a sorted count.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Helper function (from Task 2) to recursively fetch all hot article titles.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        'User-Agent': 'alx-project-advanced-api:v1.0.0 (by /u/dumethode)'
    }
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        if response.status_code != 200:
            return None

        data = response.json().get("data")
        children = data.get("children")

        if not children:
            return hot_list

        for post in children:
            hot_list.append(post.get("data").get("title"))

        next_after = data.get("after")

        if next_after is not None:
            return recurse(subreddit, hot_list, next_after)

        return hot_list

    except requests.exceptions.RequestException:
        return None


def count_words(subreddit, word_list, count_dict={}):
    """
    Queries Reddit API, parses titles of all hot articles, and prints a
    sorted count of given keywords.
    """
    # Use the recursive helper function to get all titles
    all_titles = recurse(subreddit)

    if not all_titles:
        # If the subreddit is invalid or has no posts, print nothing
        return

    # Normalize the word list: lowercase, remove duplicates (keep order for counting later)
    # The requirement says if word_list contains duplicates, the final count 
    # should be the sum. We iterate the original list to handle this.
    normalized_keywords = [word.lower() for word in word_list]
    
    # Initialize count dictionary with 0s
    if not count_dict:
        for word in normalized_keywords:
            count_dict[word] = 0

    # Process all titles
    for title in all_titles:
        # Split the title into words, convert to lowercase
        title_words = [w.lower() for w in title.split()]
        
        for title_word in title_words:
            # Strip non-alphanumeric characters from the end of the word
            # This handles 'java.' or 'java!' but keeps 'javascript' intact.
            clean_title_word = title_word.strip('._-!').lower()

            for keyword in normalized_keywords:
                if clean_title_word == keyword:
                    count_dict[keyword] += 1
    
    # Filter out keywords with a count of 0
    filtered_counts = {k: v for k, v in count_dict.items() if v > 0}

    # Sort the results:
    # 1. Descending by count (value)
    # 2. Ascending alphabetically by keyword (key)
    sorted_items = sorted(
        filtered_counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    # Print the results
    for word, count in sorted_items:
        print(f"{word}: {count}")

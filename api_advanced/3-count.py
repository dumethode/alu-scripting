#!/usr/bin/python3
"""
Module that recursively queries the Reddit API, parses titles of hot articles,
and prints a sorted count of given keywords
"""
import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Recursively queries the Reddit API, parses titles of hot articles,
    and prints a sorted count of given keywords.
    
    Args:
        subreddit: name of the subreddit
        word_list: list of keywords to count
        after: token for pagination
        word_count: dictionary to accumulate word counts
        
    Returns:
        None (prints sorted word counts)
    """
    if word_count is None:
        word_count = {}
        # Initialize word_count with lowercase keywords
        for word in word_list:
            word_count[word.lower()] = 0
    
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/91.0.4472.124 Safari/537.36'}
    params = {'limit': 100}
    
    if after:
        params['after'] = after
    
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            after = data.get('data', {}).get('after')
            
            for post in posts:
                title = post.get('data', {}).get('title', '').lower()
                words = title.split()
                
                for word in words:
                    # Clean word of punctuation at the end
                    word = word.strip('.,!?_')
                    if word in word_count:
                        word_count[word] += 1
            
            if after:
                return count_words(subreddit, word_list, after, word_count)
            else:
                # Print results sorted by count (desc) then alphabetically
                sorted_words = sorted(word_count.items(),
                                      key=lambda x: (-x[1], x[0]))
                for word, count in sorted_words:
                    if count > 0:
                        print("{}: {}".format(word, count))
        else:
            return None
    except Exception:
        return None

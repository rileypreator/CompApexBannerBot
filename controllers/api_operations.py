"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 1/29/2024
"""

from imports.imports import praw, json, Counter, re
def api_startup(check_stats=False):
    with open('data/config.json', 'r') as config_file:
        config = json.load(config_file)

    print(config['username'])
    reddit = praw.Reddit(client_id=config['client_id'],
                     client_secret=config['client_secret'],
                     user_agent=config['user_agent'],
                     username=config['username'],
                     password=config['password'])

    subreddit = reddit.subreddit("competitiveapex")

    if check_stats:
        check_emoji(subreddit)
    
    return "success"

def check_emoji(subreddit):
    emoji_counter = Counter()
    segments = ['hot', 'new', 'top', 'controversial']
    time_filters = ['day', 'week', 'month', 'year', 'all']

    def extract_emojis(flair_text):
        return re.findall(r':(.*?):', flair_text)

    for segment in segments:
        if segment in ['top', 'controversial']:
            for time_filter in time_filters:
                for submission in getattr(subreddit, segment)(time_filter=time_filter, limit=None):
                    if submission.author_flair_text:
                        emojis = extract_emojis(submission.author_flair_text)
                        emoji_counter.update(emojis)
        else:
            for submission in getattr(subreddit, segment)(limit=None):
                if submission.author_flair_text:
                    emojis = extract_emojis(submission.author_flair_text)
                    emoji_counter.update(emojis)

    # Print the collected emoji data
    for emoji, count in emoji_counter.items():
        print(f"Emoji: :{emoji}:, Count: {count}")
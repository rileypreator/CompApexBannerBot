"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 1/29/2024
"""

from imports.imports import praw, json, Counter, re, datetime
def api_startup(check_stats=False):
    try:
        reddit = grab_reddit_praw()

        # Verify that the session is working with a print message of the Bot's username
        print(reddit.user.me())
    except:
        print("Error: Could not connect to Reddit. Check your config file.")
        return "failure"

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

def grab_reddit_praw():
    # Grab all necessary reddit client information from the config file
    with open('data/config.json', 'r') as config_file:
        config = json.load(config_file)

    reddit = praw.Reddit(client_id=config['client_id'],
                client_secret=config['client_secret'],
                user_agent=config['user_agent'],
                username=config['username'],
                password=config['password'])

    return reddit

def update_banner():
    try:
        reddit = grab_reddit_praw()
        subreddit = reddit.subreddit("competitiveapex")

        banner_image_path = "./images/final_background.png"

        with open(banner_image_path, "rb") as image:
            banner_url = subreddit.stylesheet.upload_banner("images/final_background.png")

    # Update the subreddit's banner using the uploaded image URL
        subreddit.mod.update(banner=banner_url)
        print("Banner updated!")
    except:
        print("Error: Could not connect to Reddit. Check your config file.")
        return "failure"


def grab_flair_list():
    reddit = grab_reddit_praw()
    subreddit = reddit.subreddit("competitiveapex")

    flair_list = []
    # Open a file in write mode
    with open('data/flairlist.txt', 'w', encoding='utf-8') as file:
        for flair in subreddit.flair(limit=None):
            flair_list.append(flair)
            print(flair)

        flair_list = sorted(flair_list, key=lambda x: x['user'].name)
        for flair in flair_list:
            if not (flair["flair_text"] == None):
                file.write(flair['user'].name + "'s flair: " + flair["flair_text"] + "\n")

    print("Array saved to flairlist.txt")
    return flair_list

def grab_user_activity(username):
    reddit = grab_reddit_praw()
    subreddit = reddit.subreddit("competitiveapex")

    user = reddit.redditor(username)

    # Initialize variables to store the latest times
    latest_post_time = None
    latest_comment_time = None

    # Check the user's submissions
    for submission in user.submissions.new(limit=None):
        if submission.subreddit.display_name.lower() == subreddit.display_name.lower():
            latest_post_time = submission.created_utc
            break  # Stop checking after finding the latest submission

    # Check the user's comments
    for comment in user.comments.new(limit=None):
        if comment.subreddit.display_name.lower() == subreddit.display_name.lower():
            latest_comment_time = comment.created_utc
            break  # Stop checking after finding the latest comment


    # Compare and find the latest activity (post or comment)
    if latest_post_time or latest_comment_time:
        latest_activity_time = max(filter(None, [latest_post_time, latest_comment_time]))
        latest_activity_datetime = datetime.utcfromtimestamp(latest_activity_time)
        print(f"Latest activity in r/{subreddit} by u/{username}: {latest_activity_datetime}")
    else:
        print(f"No activity in r/{subreddit} found for u/{username}")

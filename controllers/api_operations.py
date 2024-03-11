"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 3/11/2024
"""

from imports.imports import praw, json, Counter, re, datetime
def api_startup(subreddit, check_stats=False):
    try:
        reddit = grab_reddit_praw()

        # Verify that the session is working with a print message of the Bot's username
        print(reddit.user.me())
        print("Reddit API is connected. Please operate the program with another script execution")
    except:
        print("Error: Could not connect to Reddit. Check your config file.")
        return "failure"

    if check_stats:
        print("Checking stats... Please wait a few minutes")
        check_emoji(subreddit)
    else:
        print("Ran basic api startup operation. Please check parameters")

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

def update_banner(subreddit):
    try:
        reddit = grab_reddit_praw()
        subreddit = reddit.subreddit(subreddit)

        banner_image_path = "./images/final_background.png"

        with open(banner_image_path, "rb") as image:
            banner_url = subreddit.stylesheet.upload_banner("images/final_background.png")

    # Update the subreddit's banner using the uploaded image URL
        subreddit.mod.update(banner=banner_url)
        print("Banner updated!")
    except:
        print("Error: Could not connect to Reddit. Check your config file.")
        return "failure"


def grab_flair_list(subreddit):
    reddit = grab_reddit_praw()
    subreddit = reddit.subreddit(subreddit)

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

def grab_user_activity(username, subreddit):
    reddit = grab_reddit_praw()
    subreddit = reddit.subreddit(subreddit)

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

def get_approved_users(subreddit):

    # Get Reddit information
    reddit = grab_reddit_praw()
    subreddit = reddit.subreddit(subreddit)

    # Open approved users and check comments
    with open('data/pin_user_comments.json', 'r') as user_file:
        users = json.load(user_file)

    # Print list of users that will have comments pinned
    users = users['approved_users']
    print("List of comment approved users")
    for user in users:
        print(user)

    # Create a stream for the bot to listen to
    for comment in subreddit.stream.comments(skip_existing=True):
        # If the comment is written by an approved user proceed to add it to the pinned comment
        if comment.author.name in users:
            print(f"User {comment.author.name} commented.")


            # Iterate through submission's comments to see if there is already a pinned comment by the bot
            pinned_comment_found = False
            for bot_comment in submission.comments:
                if bot_comment.author.name == "CompApexBot":
                    pinned_comment = bot_comment.body
                    pinned_comment += "\n"
                    pinned_comment += write_pinned_comment(comment)
                    bot_comment.edit(pinned_comment)

                    print("Posted comment")
                    print(pinned_comment)

                    break
                else:
                    new_comment = "This is a list of the comments made by Respawn Developers. Click on each comment's appropriate link to go the corresponding thread.\n"
                    new_comment += write_pinned_comment(comment)
                    submitted_comment = submission.reply(new_comment)
                    submitted_comment.mod.distinguish(sticky=True)
                    submitted_comment.mod.lock()

                    print("Posted comment")
                    print(new_comment)

                    # Change post's flair to be the Developer Response
                    submission = comment.submission
                    flairs = submission.flair.choices()
                    flair_id = get_dev_flair(flairs)
                    print("Adding dev flair: " + flair_id)
                    submission.flair.select(flair_id)

def write_pinned_comment(comment):
    # Write and link to the original comment by the user
    written_by_comment = "* [Comment by "
    written_by_comment += comment.author.name
    written_by_comment += "]("
    written_by_comment += comment.permalink
    written_by_comment += "):\n"

    # Quote the response here
    comment_body = "> "
    comment_body += comment.body
    comment_body += "\n"

    entire_comment = written_by_comment
    entire_comment += comment_body
    entire_comment += "\n"

    return entire_comment

def get_dev_flair(flairs):
    for flair in flairs:
        flair_string = flair["flair_text"]
        if flair_string.startswith("Dev"):
            return flair["flair_template_id"]
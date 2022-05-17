# Yagato
# 16/5/2022

import datetime
import pandas as pd
import praw
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('PASSWORD')

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD,
    user_agent=USER_AGENT)

def create_csv(flair):
    day = datetime.date.today().strftime("%d-%m-%Y")
    filename = flair + "_issues_" + day + ".csv"

    posts = []
    subreddit = reddit.subreddit('HoloNews').search(f'flair:"{flair} Issue"')

    for post in subreddit:
        date = datetime.datetime.fromtimestamp(post.created_utc)
        posts.append([post.title, post.score, post.ups, post.downs, post.upvote_ratio, 
            post.url, post.num_comments, date])

    posts = pd.DataFrame(posts, columns=['title', 'score', 'upvotes', 'downvotes', 'ratio', 
        'url', 'num_comments', 'created'])
    posts['created'] = pd.to_datetime(posts['created'])
    posts = posts.sort_values(by='created', ascending=False)

    posts.to_csv(rf'csv/{filename}', index=False, header=True, encoding='utf-8-sig')

    #print(posts)


# TO-DO
"""
- Share count
- View count 
"""

# Yagato
# 16/5/2022

import datetime
import pandas as pd
import os
from dotenv import load_dotenv
import asyncpraw

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('PASSWORD')

reddit = asyncpraw.Reddit(
    client_id=CLIENT_ID, 
    client_secret=CLIENT_SECRET, 
    username=USERNAME, 
    password=PASSWORD,
    user_agent=USER_AGENT,
    check_for_async=False
)


async def create_csv_reddit(flair):
    day = datetime.date.today().strftime("%d-%m-%Y")
    filename = flair + "_issues_" + day + ".csv"

    posts = []
    subreddit = await reddit.subreddit('HoloNews')
    subreddit = subreddit.search(f'flair:"{flair} Issue"')

    async for post in subreddit:
        date = datetime.datetime.fromtimestamp(post.created_utc)
        posts.append([post.title, post.score, post.ups, post.downs, post.upvote_ratio, 
            post.url, post.num_comments, date])

    posts = pd.DataFrame(posts, columns=['title', 'score', 'upvotes', 'downvotes', 'ratio', 
        'url', 'num_comments', 'created'])
    posts['created'] = pd.to_datetime(posts['created'])
    posts = posts.sort_values(by='created', ascending=False)

    posts.to_csv(rf'csv/reddit_scrapper/{filename}', index=False, header=True, encoding='utf-8-sig')


# TO-DO
"""
- Share count
- View count 
"""

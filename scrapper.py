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

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

posts = []
subreddit = reddit.subreddit('HoloNews').search('flair:"ES Issue"')

for post in subreddit:
    date = datetime.datetime.fromtimestamp(post.created_utc)
    posts.append([post.title, post.score, post.ups, post.downs, post.upvote_ratio, 
        post.url, post.num_comments, date])

posts = pd.DataFrame(posts, columns=['title', 'score', 'upvotes', 'downvotes', 'ratio', 
    'url', 'num_comments', 'created'])

posts.to_csv(r'csv/es_issues.csv', index=False, header=True, encoding='utf-8-sig')

print(posts)



""" 
- Votos *
- Score (upvotes - down votes) *
- Número de comentarios *
- Cantidad de veces que fue compartido
- Número de vistas 
- Porcentaje de upvote *
- Fecha de publicación *
"""

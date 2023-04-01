# Yagato
# 1/4/2023

import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json
import pandas as pd
import time
import math

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)


def get_subscribers(channel_id):
    req = youtube.channels().list(
        part='statistics',
        id=channel_id
    )

    res = req.execute()

    subscribers = res['items'][0]['statistics']['subscriberCount']

    return subscribers


def get_channel_name(channel_id):
    req = youtube.channels().list(
        part='snippet',
        id=channel_id
    )

    res = req.execute()

    channe_name = res['items'][0]['snippet']['title']

    return channe_name


def load_channel_ids():
    file = open('talents.json')

    talents = json.load(file)

    channel_ids = []

    for i in talents['talents']:
        channel_ids.append(i['id'])

    return channel_ids


def load_talent_generations():
    file = open('talents.json')

    talents = json.load(file)

    generations = []

    for i in talents['talents']:
        generations.append(i['generation'])

    return generations


def fetch_data():
    print("Loading data...") 
    channel_ids = load_channel_ids()
    generations = load_talent_generations()
    
    index = []
    channel_names = []
    channel_subscribers = []

    counter = 0

    print("Starting fetching process...")
    start = time.perf_counter()

    for i in channel_ids:
        index.append(counter)
        channel_names.append(get_channel_name(i))
        channel_subscribers.append(get_subscribers(i))
        
        counter += 1

        if(counter == math.ceil(len(channel_ids)/2)):
            print("Almost there...")

    end = time.perf_counter()
    print(f"Fetching process finished in {end - start:0.4f} seconds.")

    zipped = zip(index, channel_names, channel_subscribers, generations)

    return zipped

    

def create_csv_talents(filename, day):
    zipped = fetch_data()

    print("Creating CSV...")
    dataframe = []
    columns_names = ['index', 'name', 'subs', 'generation', 'date']

    for index, name, subs, gens in zipped:
        dataframe.append([index, name, subs, gens, day])

    dataframe = pd.DataFrame(dataframe, columns=columns_names)

    dataframe = dataframe.sort_values(by='index')

    dataframe.to_csv(rf'csv/yt_data/{filename}', index=False, header=True, encoding='utf-8-sig')

    print(f"CSV created in csv/yt-data/{filename}")
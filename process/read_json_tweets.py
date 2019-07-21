import csv
import json
import sys
import warnings
import os

import pandas as pd
import numpy as np
import re
from tqdm import tqdm

warnings.simplefilter(action="ignore", category=FutureWarning)


json_folder = sys.argv[1]
output_folder = sys.argv[2]
output_folder = os.path.abspath(output_folder)


def db_init():
    global df_users
    global df_tweets
    global df_hashtags
    global df_users_mentions
    global df_retweet_users
    global hashtags_docs

    # initialisation of databases, df files

    d_users = {
        "user_id": [],
        "name": [],
        "screen_name": [],
        "location": [],
        "description": [],
        "url": [],
        "followers_count": [],
        "friends_count": [],
        "listed_count": [],
        "created_at": [],
        "favourites_count": [],
        "geo_enabled": [],
        "verified": [],
        "statuses_count": [],
        "lang": [],
        "contributors_enabled": [],
    }
    df_users = pd.DataFrame(data=d_users)

    d_tweets = {
        "tweet_id": [],
        "created_at": [],
        "text": [],
        "truncated": [],
        "source": [],
        "in_reply_to_status_id": [],
        "in_reply_to_user_id": [],
        "in_reply_to_screen_name": [],
        "user_id": [],
        "geo": [],
        "coordinates": [],
        "place": [],
        "contributors": [],
        "is_quote_status": [],
        "retweet_count": [],
        "favorite_count": [],
        "favorited": [],
        "retweeted": [],
        "lang": [],
    }
    df_tweets = pd.DataFrame(data=d_tweets)

    hashtag_doc = {"tweet_id": [], "hashtags_as_string": []}
    hashtags_docs = pd.DataFrame(data=hashtag_doc)

    d_hashtags = {"hashtag": [], "tweet_id": []}
    df_hashtags = pd.DataFrame(data=d_hashtags)

    d_users_mentions = {
        "tweet_id": [],
        "mentioned_user_id": [],
        "user_id": [],
        "mentioned_screen_name": [],
        "screen_name": [],
    }
    df_users_mentions = pd.DataFrame(data=d_users_mentions)

    d_retweet_users = {
        "user_id": [],
        "original_user_id": [],
        "tweet_id": [],
        "original_tweet_id": [],
        "user_screen_name": [],
        "original_user_screen_name": [],
    }
    df_retweet_users = pd.DataFrame(data=d_retweet_users)


def is_a_retweet(tweet):
    #### returns a true if the tweet is a retweet, false if it's an original tweets
    return tweet.get("retweeted_status", None) != None


# store all hashtags related to a tweet
def store_hashtag(tweet):
    global df_hashtags
    global hashtags_docs
    if is_a_retweet(tweet):
        store_hashtag(tweet["retweeted_status"])
    else:
        hashtags_as_string = ""
        for raw_hash in tweet["entities"]["hashtags"]:
            df_hashtags = df_hashtags.append(
                {"hashtag": raw_hash["text"], "tweet_id": tweet["id_str"]},
                ignore_index=True,
            )
            hashtags_as_string += " " + raw_hash["text"]
        hashtags_docs = hashtags_docs.append(
            {"tweet_id": tweet["id_str"], "hashtags_as_string": hashtags_as_string},
            ignore_index=True,
        )


# store all user mentions contained in the tweet
def store_user_mentions(tweet):
    global df_users_mentions
    tweet_id = tweet["id_str"]
    if is_a_retweet(tweet):
        store_user_mentions(tweet["retweeted_status"])
    else:
        for raw_mention in tweet["entities"]["user_mentions"]:
            m_screen_name = raw_mention["screen_name"]

            m_user_id = raw_mention["id_str"]
            df_users_mentions = df_users_mentions.append(
                {
                    "tweet_id": tweet_id,
                    "mentioned_user_id": m_user_id,
                    "user_id": tweet["user"]["id_str"],
                    "mentioned_screen_name": m_screen_name,
                    "screen_name": tweet["user"]["screen_name"],
                },
                ignore_index=True,
            )


# store the author of the tweet
def store_user(tweet):
    global df_users
    user = tweet["user"]

    if is_a_retweet(tweet):
        store_user(tweet["retweeted_status"])
    else:
        if user["id_str"] not in df_users["user_id"].values:
            d_user = {
                "user_id": user["id_str"],
                "name": user["name"],
                "screen_name": user["screen_name"],
                "location": user["location"],
                "description": user["description"],
                "url": user["url"],
                "followers_count": user["followers_count"],
                "friends_count": user["friends_count"],
                "listed_count": user["listed_count"],
                "created_at": user["created_at"],
                "favourites_count": user["favourites_count"],
                "geo_enabled": user["geo_enabled"],
                "verified": user["verified"],
                "statuses_count": user["statuses_count"],
                "lang": user["lang"],
                "contributors_enabled": user["contributors_enabled"],
            }
            df_users = df_users.append(d_user, ignore_index=True)


# store the content of the tweet
def store_tweet(tweet):
    global df_tweets
    if tweet.get("full_text"):
        text = re.sub(
            r"http\S+", "", tweet.get("full_text")
        )  ## Removes URLs from full text
    else:
        text = ""
    if tweet["id_str"] not in df_tweets["tweet_id"].values:
        if is_a_retweet(tweet):
            store_tweet(tweet["retweeted_status"])

        else:
            df_tweets = df_tweets.append(
                {
                    "tweet_id": tweet["id_str"],
                    "created_at": tweet["created_at"],
                    "text": text,
                    "truncated": tweet["truncated"],
                    "source": tweet["source"],
                    "in_reply_to_status_id": tweet["in_reply_to_status_id_str"],
                    "in_reply_to_user_id": tweet["in_reply_to_user_id_str"],
                    "in_reply_to_screen_name": tweet["in_reply_to_screen_name"],
                    "user_id": tweet["user"]["id_str"],
                    "geo": tweet["geo"],
                    "coordinates": tweet["coordinates"],
                    "place": tweet["place"],
                    "contributors": tweet["contributors"],
                    "is_quote_status": tweet["is_quote_status"],
                    "retweet_count": tweet["retweet_count"],
                    "favorite_count": tweet["favorite_count"],
                    "favorited": tweet["favorited"],
                    "retweeted": tweet["retweeted"],
                    "lang": tweet["lang"],
                },
                ignore_index=True,
            )


# called when the tweet is a retweet: store the original author of the tweet as well as the user who retweeted it,
# and the original id of the tweet
def store_retweet_user(tweet):
    global df_retweet_users

    df_retweet_users = df_retweet_users.append(
        {
            "user_id": tweet["user"]["id_str"],
            "original_user_id": tweet["retweeted_status"]["user"]["id_str"],
            "tweet_id": tweet["id_str"],
            "original_tweet_id": tweet["retweeted_status"]["id_str"],
            "user_screen_name": tweet["user"]["screen_name"],
            "original_user_screen_name": tweet["retweeted_status"]["user"][
                "screen_name"
            ],
        },
        ignore_index=True,
    )


def process_json_tweet(tweet):
    tweet = json.load(tweet)

    store_tweet(tweet)
    store_user(tweet)
    store_hashtag(tweet)
    store_user_mentions(tweet)

    if is_a_retweet(tweet):
        store_retweet_user(tweet)
    # store tweets only when they are original tweets


def read_json_folder(path_to_json):
    json_files = [
        pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith(".json")
    ]
    for json_file in tqdm(json_files):

        with open(os.path.join(path_to_json, json_file)) as tweet:

            process_json_tweet(tweet)


def df_to_csv(output_folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    newpath = os.path.join(dir_path, output_folder)
    if not os.path.exists(newpath):
        os.makedirs(newpath, exist_ok=True)

    df_users.to_csv(os.path.join(output_folder, "users.csv"), index=False)
    df_retweet_users.to_csv(
        os.path.join(output_folder, "retweet_users.csv"), index=False
    )
    df_tweets.to_csv(os.path.join(output_folder, "tweets.csv"), index=False)
    df_users_mentions.to_csv(
        os.path.join(output_folder, "users_mentions.csv"), index=False
    )
    df_hashtags.to_csv(os.path.join(output_folder, "hashtags.csv"), index=False)
    hashtags_docs.to_csv(os.path.join(output_folder, "hashtags_docs.csv"), index=False)


def main():
    #### loading the databases
    db_init()
    read_json_folder(json_folder)
    df_to_csv(output_folder)


if __name__ == "__main__":
    main()

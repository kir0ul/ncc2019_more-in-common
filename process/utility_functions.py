# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import json
import re


# +
# databases initialisations
def db_init():
    global df_users
    global df_tweets
    global df_hashtags
    global df_users_mentions
    global df_retweet_users

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

    d_hashtags = {"hashtag": [], "tweet_id": []}
    df_hashtags = pd.DataFrame(data=d_hashtags)

    d_users_mentions = {"tweet_id": [], "user_id": [], "screen_name": [], "name": []}
    df_users_mentions = pd.DataFrame(data=d_users_mentions)

    d_retweet_users = {"user_id": [], "original_user_id": [], "original_tweet_id": []}
    df_retweet_users = pd.DataFrame(data=d_retweet_users)


# -

rt = 0


def is_a_retweet(tweet):
    #### returns a true if the tweet is a retweet, false if it's an original tweets
    global rt
    rt += 1
    return tweet.get("retweeted_status", None) != None


# +
# store all hashtags related to a tweet
def store_hashtag(tweet):
    global df_hashtags
    for raw_hash in tweet["entities"]["hashtags"]:
        df_hashtags = df_hashtags.append(
            {"hashtag": raw_hash["text"], "tweet_id": tweet["id_str"]},
            ignore_index=True,
        )


# store all user mentions contained in the tweet
def store_user_mentions(tweet):
    global df_users_mentions
    tweet_id = tweet["id_str"]
    for raw_mention in tweet["entities"]["user_mentions"]:
        screen_name = raw_mention["screen_name"]
        name = raw_mention["name"]
        user_id = raw_mention["id_str"]
        df_users_mentions = df_users_mentions.append(
            {
                "tweet_id": tweet_id,
                "user_id": user_id,
                "screen_name": screen_name,
                "name": name,
            },
            ignore_index=True,
        )


# store the author of the tweet
def store_user(tweet):
    global df_users
    user = tweet["user"]
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
    text = re.sub(r"http\S+", "", tweet["full_text"])  ## Removes URLs from full text
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
    if is_a_retweet(tweet):
        df_retweet_users = df_retweet_users.append(
            {
                "user_id": tweet["user"]["id_str"],
                "original_user_id": tweet["retweeted_status"]["user"]["id_str"],
                "original_tweet_id": tweet["retweeted_status"]["id_str"],
            },
            ignore_index=True,
        )


##Never used
##T0D0: proper encapsulation
def store_influent_users(n):
    # n is the number of influent users return
    df_favorite_count = (
        df_tweets.groupby(["user_id"])["favorite_count"]
        .agg("sum")
        .sort_values(ascending=False)
        .head()
    )
    for i in range(n):
        d_influent_users = {
            "user_id": df_favorite_count[0],
            "name": [],
            "retweet_count": [],
            "favorite_count": [],
            "description": [],
        }


# -


def process_json_tweet(tweet):
    tweet = json.load(tweet)

    if is_a_retweet(tweet):
        store_retweet_user(tweet)

    else:  # store tweets only when they are original tweets
        store_tweet(tweet)
        store_user(tweet)
        store_hashtag(tweet)
        store_user_mentions(tweet)


# +
####request to Twitter API
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify = True)

# for tweet in tweepy.Cursor(api.search,q="#"+input_hashtag,#count=n_tweets,    #this is a search by hashtags
#                           lang=language,
#                           since=since_date, tweet_mode='extended').items():

#    with open('tweets/tweet'+str(tweet.id)+'.json', 'w', encoding='utf8') as file:
#        ####you need to create a 'tweets' folder
#        tweet_json = tweet._json
#        json.dump(tweet_json, file)

# -

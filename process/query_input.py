import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import sys

pd.options.display.max_colwidth = 1000
from pandas.io.json import json_normalize

csv_folder = sys.argv[1]
request = sys.argv[2]
query_input = sys.argv[3]


def read_all_csv(csv_folder):
    global df_users
    global df_tweets
    global df_hashtags
    global df_users_mentions
    global df_retweet_users
    global hashtags_docs

    df_users = pd.read_csv(csv_folder + "\\" + "users.csv")
    df_tweets = pd.read_csv(csv_folder + "\\" + "tweets.csv")
    df_hashtags = pd.read_csv(csv_folder + "\\" + "hashtags.csv")
    df_users_mentions = pd.read_csv(csv_folder + "\\" + "users_mentions.csv")
    df_retweet_users = pd.read_csv(csv_folder + "\\" + "retweet_users.csv")
    hashtags_docs = pd.read_csv(csv_folder + "\\" + "hashtags_docs.csv")


def get_tweet_by(name):
    df_tweets_user_info = df_tweets.set_index("user_id").join(
        df_users.drop(columns=["created_at", "lang"]).set_index("user_id")
    )
    df_tweets_user_info = df_tweets_user_info[
        df_tweets_user_info["screen_name"] == name
    ]
    df_tweets_user_info = df_tweets_user_info[
        ["tweet_id", "text", "created_at", "favorite_count", "retweet_count"]
    ]
    print(df_tweets_user_info)
    return df_tweets_user_info


def get_related_hash_by(name):
    df_tweets_hashtags = df_hashtags.set_index("tweet_id").join(
        df_tweets.set_index("tweet_id")
    )
    df_tw_hash_user = df_tweets_hashtags.set_index("user_id").join(
        df_users.drop(columns=["created_at", "lang"]).set_index("user_id")
    )
    df_aggretated = (
        df_tw_hash_user.groupby(["screen_name", "hashtag"]).size().reset_index()
    )
    df_aggretated.columns = ["Name", "#", "Used"]
    df_aggretated[df_aggretated["Name"] == name][["#", "Used"]].sort_values(
        "Used", ascending=False
    )


def main():

    read_all_csv(csv_folder)

    options = {
        "tweet_by": get_tweet_by(query_input),
        "related_hash_by": get_related_hash_by(query_input),
    }
    try:
        options[request]

    except KeyError:
        print(
            "Error: "
            + request
            + " is not a recognized request. Available requests are: tweet_by, related_hash_by"
        )


if __name__ == "__main__":
    main()

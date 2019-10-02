import os
import pandas as pd

pd.options.display.max_colwidth = 1000


class Query:
    def __init__(self, csv_folder):
        self.df_users = pd.read_csv(os.path.join(csv_folder, "users.csv"))
        self.df_tweets = pd.read_csv(os.path.join(csv_folder, "tweets.csv"))
        self.df_hashtags = pd.read_csv(os.path.join(csv_folder, "hashtags.csv"))
        self.df_users_mentions = pd.read_csv(
            os.path.join(csv_folder, "users_mentions.csv")
        )
        self.df_retweet_users = pd.read_csv(
            os.path.join(csv_folder, "retweet_users.csv")
        )
        self.hashtags_docs = pd.read_csv(os.path.join(csv_folder, "hashtags_docs.csv"))

    def get_tweet_by(self, name):
        df_tweets_user_info = self.df_tweets.set_index("user_id").join(
            self.df_users.drop(columns=["created_at", "lang"]).set_index("user_id")
        )
        df_tweets_user_info = df_tweets_user_info[
            df_tweets_user_info["screen_name"] == name
        ]
        df_tweets_user_info = df_tweets_user_info[
            ["tweet_id", "text", "created_at", "favorite_count", "retweet_count"]
        ]
        print(df_tweets_user_info.head())
        return df_tweets_user_info

    def get_related_hash_by(self, name):
        df_tweets_hashtags = self.df_hashtags.set_index("tweet_id").join(
            self.df_tweets.set_index("tweet_id")
        )
        df_tw_hash_user = df_tweets_hashtags.set_index("user_id").join(
            self.df_users.drop(columns=["created_at", "lang"]).set_index("user_id")
        )
        df_aggretated = (
            df_tw_hash_user.groupby(["screen_name", "hashtag"]).size().reset_index()
        )
        df_aggretated.columns = ["Name", "#", "Used"]
        df_aggretated[df_aggretated["Name"] == name][["#", "Used"]].sort_values(
            "Used", ascending=False
        )

import pandas as pd
import os

pd.options.display.max_colwidth = 1000


class Aggregate:
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

    def get_top_rt_users(self):
        """Top retweeted users"""
        df_most_retweeted_users = (
            self.df_tweets.groupby(["user_id"])["retweet_count"]
            .agg("sum")
            .sort_values(ascending=False)
            .reset_index()
            .head(15)
        )
        df_most_retweeted_users["retweet_count"] = df_most_retweeted_users[
            "retweet_count"
        ].astype("int32")
        df_most_retweeted_users["user_id"] = df_most_retweeted_users["user_id"].astype(
            object
        )
        df_most_retweeted_users_with_info = (
            df_most_retweeted_users.set_index("user_id")
            .join(self.df_users.set_index("user_id"))
            .drop_duplicates()
            .sort_values("retweet_count", ascending=False)
        )
        df_tweets_by_user = (
            self.df_tweets.groupby(["user_id"]).size().to_frame().reset_index()
        )
        df_most_retweeted_users_with_info = (
            df_most_retweeted_users_with_info.join(
                df_tweets_by_user.set_index("user_id")
            )
            .drop_duplicates()
            .sort_values("retweet_count", ascending=False)
        )
        top_influencers_rt = df_most_retweeted_users_with_info[
            [
                "screen_name",
                "description",
                "followers_count",
                "friends_count",
                "retweet_count",
                0,
            ]
        ]
        top_influencers_rt.columns = [
            "Name",
            "Description",
            "Number of followers",
            "Number of friends",
            "Number of retweets",
            "Number of tweets",
        ]
        top_influencers_rt = top_influencers_rt.reset_index().drop(columns=["user_id"])
        top_influencers_rt["Number of followers"] = top_influencers_rt[
            "Number of followers"
        ].astype(int)
        top_influencers_rt["Number of friends"] = top_influencers_rt[
            "Number of friends"
        ].astype(int)
        top_influencers_rt.loc[:, "Retweet Tweet Ratio"] = (
            top_influencers_rt.loc[:, "Number of retweets"]
            / top_influencers_rt.loc[:, "Number of tweets"]
        )

        print(top_influencers_rt.head())
        return top_influencers_rt

    def get_top_fav_users(self):
        """Top favorited users"""
        df_most_favorited_users = (
            self.df_tweets.groupby(["user_id"])["favorite_count"]
            .agg("sum")
            .sort_values(ascending=False)
            .reset_index()
            .head(15)
        )
        df_most_favorited_users["favorite_count"] = df_most_favorited_users[
            "favorite_count"
        ].astype("int32")
        df_most_favorited_users["user_id"] = df_most_favorited_users["user_id"].astype(
            object
        )
        df_most_favorited_users_with_info = (
            df_most_favorited_users.set_index("user_id")
            .join(self.df_users.set_index("user_id"))
            .drop_duplicates()
            .sort_values("favorite_count", ascending=False)
        )
        df_tweets_by_user = (
            self.df_tweets.groupby(["user_id"]).size().to_frame().reset_index()
        )
        df_most_favorited_users_with_info = (
            df_most_favorited_users_with_info.join(
                df_tweets_by_user.set_index("user_id")
            )
            .drop_duplicates()
            .sort_values("favorite_count", ascending=False)
        )
        top_influencers_fav = df_most_favorited_users_with_info[
            [
                "screen_name",
                "description",
                "followers_count",
                "friends_count",
                "favorite_count",
                0,
            ]
        ]
        top_influencers_fav.columns = [
            "Name",
            "Description",
            "Number of followers",
            "Number of friends",
            "Number of favorites",
            "Number of tweets",
        ]
        top_influencers_fav = top_influencers_fav.reset_index().drop(
            columns=["user_id"]
        )
        top_influencers_fav["Number of followers"] = top_influencers_fav[
            "Number of followers"
        ].astype(int)
        top_influencers_fav["Number of friends"] = top_influencers_fav[
            "Number of friends"
        ].astype(int)
        top_influencers_fav.loc[:, "Like Tweet Ratio"] = (
            top_influencers_fav.loc[:, "Number of favorites"]
            / top_influencers_fav.loc[:, "Number of tweets"]
        )

        print(top_influencers_fav.head())
        return top_influencers_fav

    def gen_stats(self):
        """Returns the number of unique tweets in the database which
        have been tweeted between min_date and max_date,
        number of retweets, number of favorites"""
        d = pd.to_datetime(self.df_tweets["created_at"])
        min_date = d.min()
        max_date = d.max()
        return (
            len(self.df_tweets.index),
            min_date,
            max_date,
            int(self.df_tweets["retweet_count"].sum()),
            int(self.df_tweets["favorite_count"].sum()),
        )

    def top_hashtags(self):
        """Top co-tweeted hashtags"""

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
        df_total_hashtag = (
            df_aggretated.groupby("#")
            .size()
            .sort_values(0, ascending=False)
            .reset_index()
        )
        df_total_hashtag.columns = ["#", "count"]
        print(df_total_hashtag.head())
        return df_total_hashtag

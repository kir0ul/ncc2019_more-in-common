import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import sys

pd.options.display.max_colwidth = 1000
from pandas.io.json import json_normalize

csv_folder = sys.argv[1]
request = sys.argv[2]



def read_all_csv(csv_folder):
	global df_users
	global df_tweets
	global df_hashtags
	global df_users_mentions
	global df_retweet_users
	global hashtags_docs

	df_users = pd.read_csv(csv_folder + '\\' + 'users.csv')
	df_tweets = pd.read_csv(csv_folder + '\\' + 'tweets.csv')
	df_hashtags = pd.read_csv(csv_folder + '\\' + 'hashtags.csv')
	df_users_mentions = pd.read_csv(csv_folder + '\\' + 'users_mentions.csv')
	df_retweet_users = pd.read_csv(csv_folder + '\\' + 'retweet_users.csv')
	hashtags_docs = pd.read_csv(csv_folder + '\\' + 'hashtags_docs.csv')

def get_top_rt_users():
	df_most_retweeted_users = df_tweets.groupby(['user_id'])['retweet_count'].agg('sum').sort_values(ascending=False).reset_index().head(15)
	df_most_retweeted_users['retweet_count'] = df_most_retweeted_users['retweet_count'].astype('int32')
	df_most_retweeted_users['user_id'] = df_most_retweeted_users['user_id'].astype(object)
	
	df_most_retweeted_users_with_info = df_most_retweeted_users.set_index('user_id').join(df_users.set_index('user_id')).drop_duplicates().sort_values('retweet_count',ascending=False)
	top_influencers_rt = df_most_retweeted_users_with_info[['screen_name','description', 'followers_count', 'friends_count','retweet_count','Unnamed: 0']]
	top_influencers_rt.columns = ["Name","Description","Number of followers","Number of friends","Number of retweets","Number of tweets"]
	top_influencers_rt = top_influencers_rt.reset_index().drop(columns = ["user_id"]);
	top_influencers_rt['Number of followers'] = top_influencers_rt['Number of followers'].astype(int)
	top_influencers_rt['Number of friends'] = top_influencers_rt['Number of friends'].astype(int)
	top_influencers_rt.loc[:,'Retweet Tweet Ratio'] = top_influencers_rt.loc[:,"Number of retweets"]/top_influencers_rt.loc[:,"Number of tweets"]
	return top_influencers_rt

def main():

	read_all_csv(csv_folder)

	options = {'rt_users': get_top_rt_users()}
	try:
		options[request]

	except Exception:
		traceback.print_exc(file=sys.stdout)
	
        
if __name__ == '__main__':
	main()
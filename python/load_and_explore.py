# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
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

# +
import urllib3
import urllib3.request

import csv
import json
from pandas.io.json import json_normalize

import pandas as pd
pd.options.display.max_colwidth = 1000
import numpy as np
import re

import nbimporter
import utility_functions as uf

from sklearn.feature_extraction.text import CountVectorizer


# +

from importlib import reload
reload(uf)


# -


# # Loading Databases

# +
def db_init():
    global df_users
    global df_tweets
    global df_hashtags
    global df_users_mentions
    global df_retweet_users
    global hashtags_docs
    
    #initialisation of databases, df files

    d_users = {'user_id': [],
               'name':[],
               'screen_name':[],
               'location':[],
               'description':[],
               'url':[],
               'followers_count':[],
               'friends_count':[],
               'listed_count':[],
               'created_at':[],
               'favourites_count':[],
               'geo_enabled':[],
               'verified':[],
               'statuses_count':[],
               'lang':[],
               'contributors_enabled':[]
              }
    df_users = pd.DataFrame(data=d_users)

    d_tweets = {'tweet_id': [],
                'created_at': [],
                'text': [],
                'truncated': [],
                'source': [],
                'in_reply_to_status_id': [],
                'in_reply_to_user_id': [],
                'in_reply_to_screen_name': [],
                'user_id': [],
                'geo': [],
                'coordinates': [],
                'place': [],
                'contributors': [],
                'is_quote_status': [],
                'retweet_count': [],
                'favorite_count': [],
                'favorited': [],
                'retweeted': [],
                'lang': []         
               }
    df_tweets = pd.DataFrame(data=d_tweets)
    
    hashtag_doc = {'tweet_id':[], 'hashtags_as_string':[]}
    hashtags_docs = pd.DataFrame(data = hashtag_doc)
    
    d_hashtags={'hashtag': [], 'tweet_id': []}
    df_hashtags = pd.DataFrame(data=d_hashtags)

    d_users_mentions = {'tweet_id':[], 'mentioned_user_id': [], 'user_id':[], 'mentioned_screen_name':[], 'screen_name':[]}
    df_users_mentions = pd.DataFrame(data=d_users_mentions)

    d_retweet_users = {'user_id':[], 'original_user_id':[], 'original_tweet_id':[], 'user_screen_name':[], 'original_user_screen_name':[]}
    df_retweet_users= pd.DataFrame(data=d_retweet_users)

    
def is_a_retweet(tweet):
    #### returns a true if the tweet is a retweet, false if it's an original tweets 
    return tweet.get('retweeted_status',None) != None

# store all hashtags related to a tweet
def store_hashtag(tweet):
    global df_hashtags
    global hashtags_docs
    hashtags_as_string = ""
    for raw_hash in tweet['entities']['hashtags']:
            df_hashtags = df_hashtags.append({'hashtag': raw_hash['text'] ,'tweet_id':tweet['id_str']}, ignore_index=True)
            hashtags_as_string += " " + raw_hash['text']
    hashtags_docs = hashtags_docs.append({'tweet_id':tweet['id_str'], 'hashtags_as_string': hashtags_as_string}, ignore_index=True)

#store all user mentions contained in the tweet
def store_user_mentions(tweet):
    global df_users_mentions
    tweet_id = tweet['id_str']
    for raw_mention in tweet['entities']['user_mentions']:
        m_screen_name = raw_mention['screen_name']
       
        m_user_id = raw_mention['id_str']
        df_users_mentions = df_users_mentions.append({'tweet_id':tweet_id, 'mentioned_user_id': m_user_id, 'user_id':tweet['user']['id_str'], 'mentioned_screen_name':m_screen_name, 'screen_name':tweet['user']['screen_name']},ignore_index=True)

#store the author of the tweet        
def store_user(tweet):
    global df_users
    user = tweet['user']
    if user['id_str'] not in df_users['user_id'].values:
        
        d_user = {'user_id': user['id_str'],
                  'name':user['name'],
                  'screen_name':user['screen_name'],
                  'location':user['location'],
                  'description':user['description'],
                  'url':user['url'],
                  'followers_count':user['followers_count'],
                  'friends_count':user['friends_count'],
                  'listed_count':user['listed_count'],
                  'created_at':user['created_at'],
                  'favourites_count':user['favourites_count'],
                  'geo_enabled':user['geo_enabled'],
                  'verified':user['verified'],
                  'statuses_count':user['statuses_count'],
                  'lang':user['lang'],
                  'contributors_enabled':user['contributors_enabled']
                 }
        df_users = df_users.append(d_user,ignore_index=True)

#store the content of the tweet
def store_tweet(tweet):
    global df_tweets
    text = re.sub(r"http\S+", "", tweet['full_text']) ## Removes URLs from full text
    if tweet['id_str'] not in df_tweets['tweet_id'].values:
        df_tweets = df_tweets.append({'tweet_id':  tweet['id_str'],
                'created_at': tweet['created_at'],
                'text': text,
                'truncated': tweet['truncated'],
                'source': tweet['source'],
                'in_reply_to_status_id': tweet['in_reply_to_status_id_str'],
                'in_reply_to_user_id': tweet['in_reply_to_user_id_str'],
                'in_reply_to_screen_name': tweet['in_reply_to_screen_name'],
                'user_id': tweet['user']['id_str'],
                'geo': tweet['geo'],
                'coordinates': tweet['coordinates'],
                'place': tweet['place'],
                'contributors': tweet['contributors'],
                'is_quote_status': tweet['is_quote_status'],
                'retweet_count': tweet['retweet_count'],
                'favorite_count': tweet['favorite_count'],
                'favorited': tweet['favorited'],
                'retweeted': tweet['retweeted'],
                'lang': tweet['lang'] },ignore_index=True)

#called when the tweet is a retweet: store the original author of the tweet as well as the user who retweeted it,
# and the original id of the tweet
def store_retweet_user(tweet):
    global df_retweet_users
    if is_a_retweet(tweet):
        df_retweet_users = df_retweet_users.append({'user_id':tweet['user']['id_str'],
                                                    'original_user_id':tweet['retweeted_status']['user']['id_str'],
                                                    'original_tweet_id':tweet['retweeted_status']['id_str'],
                                                    'user_screen_name':tweet['user']['screen_name'],
                                                    'original_user_screen_name':tweet['retweeted_status']['user']['screen_name']
                                                   }, ignore_index=True)


# -


def process_json_tweet(tweet):
    tweet = json.load(tweet)
    
    if is_a_retweet(tweet):
        store_retweet_user(tweet)
        
    else:  #store tweets only when they are original tweets
        store_tweet(tweet)
        store_user(tweet)
        store_hashtag(tweet)
        store_user_mentions(tweet)


# +
#### loading the databases
db_init()
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
import os

path_to_json = 'tweets_twarc/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for json_file in json_files:
    
    with open(path_to_json+json_file) as tweet:
        
        process_json_tweet(tweet)
        
        
        
# -

#tweet example
df_tweets['text'].iloc[0]

d = pd.to_datetime(df_tweets['created_at'])
print(d.min())
print(d.max())
print(len(df_tweets.index)) 


#primary keys are ok if both return false
print(df_tweets.duplicated('tweet_id').any())
print(df_users.duplicated('user_id').any())


# # Coocurrence Matrix

# +
hashtags_docs
hashtags_as_strings = hashtags_docs['hashtags_as_string']
bigram_vectorizer = CountVectorizer(ngram_range=(2, 2)) 
co_occurrences = bigram_vectorizer.fit_transform(hashtags_as_strings)
sum_occ = np.sum(co_occurrences.todense(),axis=0)

#print('Pretty printig of co_occurrences count:', bigram_vectorizer.get_feature_names(),np.array(sum_occ)[0].tolist())


# +
import networkx as nx
hashGraph = nx.Graph()


pairs = bigram_vectorizer.get_feature_names()
co_occ = np.array(sum_occ)[0]
thresh = np.quantile(co_occ, 0.85)

n = len(pairs)
for i in range(n):
    pair = pairs[i].split(" ")
    w1 = pair[0]
    w2 = pair[1]
    weight = co_occ[i]
    if weight > thresh:
        hashGraph.add_edge(w1, w2, weight=weight)

d = dict(hashGraph.degree)
# -

d;

# +
import matplotlib.pyplot as plt

fig_size = plt.rcParams["figure.figsize"]
# Set figure width to 12 and height to 9
fig_size[0] = 24
fig_size[1] = 18

#nx.draw_networkx(hashGraph)
nx.draw_networkx(hashGraph, nodelist=d.keys(), node_size=[v * 100 for v in d.values()])

plt.show()
# -

from networkx.drawing.nx_agraph import graphviz_layout

# # Label Propagation and related analysis

retweet_connections = df_retweet_users.groupby(['user_screen_name', 'original_user_screen_name']).size().sort_values(ascending=False).reset_index()
retweet_connections.columns = ['user_screen_name', 'original_user_screen_name', 'count']
retweet_connections
len(retweet_connections.index)
retweet_connections = retweet_connections[retweet_connections['original_user_screen_name'] != retweet_connections['user_screen_name']]

retweet_connections[retweet_connections['original_user_screen_name'] == 'Bleu_Rochelle']


retweet_graph = nx.from_pandas_edgelist(retweet_connections, 'user_screen_name', 'original_user_screen_name', 'count')


# +
nx.draw_networkx(retweet_graph)
plt.show()

# G.remove_nodes_from(

# +
list(nx.isolates(retweet_graph))
#retweet_graph.remove_nodes_from(nx.isolates(retweet_graph))

#nx.draw_networkx(retweet_graph)
#plt.show()

#retweet_graph.degree()

# +
#from networkx_viewer import Viewer
#app = Viewer(retweet_graph)
#app.mainloop()
# -

con_comp = sorted(nx.connected_components(retweet_graph), key = len, reverse=True)
len(con_comp)


graphs = list(nx.connected_component_subgraphs(retweet_graph))
Gc = max(nx.connected_component_subgraphs(retweet_graph), key=len)
d2 = dict(Gc.degree)
n=len(d2)
pos=nx.spring_layout(Gc, k = 1/(n**(1/25)))


# +
#nx.draw_networkx(retweet_graph, nodelist=d2.keys(), node_size=[v * 50 for v in d2.values()], with_labels=False)

nx.draw_networkx(Gc, pos = pos, nodelist=d2.keys(), node_size=[v * 30 for v in d2.values()], edge_color='b',)
plt.show()
# -


import operator
sorted_nodes = sorted(d2.items(), key=operator.itemgetter(1), reverse = True)


top_nodes = sorted_nodes[:10]
top_nodes = dict(top_nodes)


top_nodes;

pos2=nx.spring_layout(Gc, k = 1/(n**(1/10)))


nx.draw_networkx(Gc, pos = pos2, nodelist=top_nodes.keys(), node_size=[v * 50 for v in top_nodes.values()], edge_color='b')


nx.write_gexf(hashGraph, "hash.gexf")


test_read = nx.read_gexf("ret_comp.gexf")

pos=nx.spring_layout(test_read)
nx.draw_networkx_labels(test_read, pos= pos)
plt.show()

plt.show()

# # Aggregations
#

# ## Top users

# +
df_most_favorited_users = df_tweets.groupby(['user_id'])['favorite_count'].agg('sum').sort_values(ascending=False).reset_index().head(15)
df_most_retweeted_users = df_tweets.groupby(['user_id'])['retweet_count'].agg('sum').sort_values(ascending=False).reset_index().head(15)
df_most_favorited_users['favorite_count'] = df_most_favorited_users['favorite_count'].astype('int32')
df_most_retweeted_users['retweet_count'] = df_most_retweeted_users['retweet_count'].astype('int32')

df_most_favorited_users['user_id'] = df_most_favorited_users['user_id'].astype(object)
df_most_retweeted_users['user_id'] = df_most_retweeted_users['user_id'].astype(object)


# -

df_most_favorited_users_with_info = df_most_favorited_users.set_index('user_id').join(df_users.set_index('user_id')).drop_duplicates().sort_values('favorite_count',ascending=False)
df_most_retweeted_users_with_info = df_most_retweeted_users.set_index('user_id').join(df_users.set_index('user_id')).drop_duplicates().sort_values('retweet_count',ascending=False)

df_most_retweeted_users_with_info.head(15)

df_most_favorited_users_with_info.head(15);

df_most_retweeted_users_with_info.reset_index()
df_most_favorited_users_with_info.reset_index();

df_tweets_by_user = df_tweets.groupby(['user_id']).size().to_frame().reset_index()
df_most_favorited_users_with_info = df_most_favorited_users_with_info.join(df_tweets_by_user.set_index('user_id')).drop_duplicates().sort_values('favorite_count',ascending=False)
df_most_retweeted_users_with_info = df_most_retweeted_users_with_info.join(df_tweets_by_user.set_index('user_id')).drop_duplicates().sort_values('retweet_count',ascending=False)

df_most_favorited_users_with_info;

top_influencers_fav = df_most_favorited_users_with_info[['screen_name','description', 'followers_count', 'friends_count','favorite_count',0]]
top_influencers_rt = df_most_retweeted_users_with_info[['screen_name','description', 'followers_count', 'friends_count','retweet_count',0]]
top_influencers_fav.columns = ["Name","Description","Number of followers","Number of friends","Number of favorites","Number of tweets"]
top_influencers_rt.columns = ["Name","Description","Number of followers","Number of friends","Number of retweets","Number of tweets"]
top_influencers_fav = top_influencers_fav.reset_index().drop(columns = ["user_id"])
top_influencers_rt = top_influencers_rt.reset_index().drop(columns = ["user_id"]);
top_influencers_fav['Number of followers'] = top_influencers_fav['Number of followers'].astype(int)
top_influencers_fav['Number of friends'] = top_influencers_fav['Number of friends'].astype(int)
top_influencers_rt['Number of followers'] = top_influencers_rt['Number of followers'].astype(int)
top_influencers_rt['Number of friends'] = top_influencers_rt['Number of friends'].astype(int)

#add ratios
top_influencers_fav.loc[:,'Like Tweet Ratio'] = top_influencers_fav.loc[:,"Number of favorites"]/top_influencers_fav.loc[:,"Number of tweets"]
top_influencers_rt.loc[:,'Retweet Tweet Ratio'] = top_influencers_rt.loc[:,"Number of retweets"]/top_influencers_rt.loc[:,"Number of tweets"]

# ## Top hashtags for this input hashtags and by users

top_influencers_fav.style.set_properties(**{'text-align': 'left'});

df_tweets_hashtags = df_hashtags.set_index('tweet_id').join(df_tweets.set_index('tweet_id'))

df_tw_hash_user = df_tweets_hashtags.set_index('user_id').join(df_users.drop(columns=['created_at', 'lang']).set_index('user_id'))

#df_aggretated = df_tw_hash_user.groupby(['user_id','hashtag']).size().reset_index()
df_aggretated = df_tw_hash_user.groupby(['screen_name','hashtag']).size().reset_index()

df_aggretated.columns = ["Name", "#", "Used"]
df_aggretated;


# +
#useful encapsulation, aint it?
def get_tweet_by_userid(user_id):
    df_tweets[df_tweets['user_id'] == 'user_id']

def get_tweet_by_username(name):
    df_tweets_user_info = df_tweets.set_index('user_id').join(df_users.drop(columns=['created_at', 'lang']).set_index('user_id'))
    df_tweets_user_info = df_tweets_user_info[df_tweets_user_info['screen_name'] == name]
    df_tweets_user_info = df_tweets_user_info[['tweet_id','text','created_at', 'favorite_count', 'retweet_count']]
    return df_tweets_user_info

def get_related_hashtags_by_username(name):
    d_name = df_aggretated[df_aggretated['Name'] == name][['#',"Used"]].sort_values("Used", ascending = False)
    return d_name
def get_user_info(name):
    return df_users[df_users['screen_name'] == name][['screen_name', 'description', 'followers_count' ]]


# -

# ## Propagation du bruit

top_influencers_fav_names = top_influencers_fav['Name'].values
top_influencers_rt_names = top_influencers_rt['Name'].values

df_most_retweeted_users_with_info = df_most_retweeted_users_with_info.reset_index()

df_retweet_users_top_account = df_retweet_users[df_retweet_users['original_user_screen_name'].isin(top_influencers_rt_names)]
rt_influencers  = df_retweet_users_top_account.groupby(['user_screen_name', 'original_user_screen_name']).size()
who_rt = rt_influencers.groupby('user_screen_name').size().sort_values(0, ascending = False).reset_index()
df_userid = df_users[['screen_name' , 'user_id']]
who_rt.columns = ['user_screen_name', 'count']
rt_influencers = rt_influencers.reset_index()

df_retweet_users;


def who_rt_who(screenname):
    return rt_influencers[rt_influencers['user_screen_name'] == screenname]


# +
# prepare data for gephi Retweet Network
df_retweet_users_edges = df_retweet_users[['user_id','original_user_id']]
df_nodes_p = df_retweet_users[['original_user_id','original_user_screen_name']].rename(columns ={'original_user_id':'user_id','original_user_screen_name': 'user_screen_name'})
df_retweet_users_nodes = pd.concat([df_retweet_users[['user_id','user_screen_name']],df_nodes_p]).drop_duplicates()

df_retweet_users_edges=df_retweet_users_edges.rename(columns ={'user_id':'Source','original_user_id':'Target'})
df_retweet_users_nodes=df_retweet_users_nodes.rename(columns ={'user_id':'id','user_screen_name':'label'})

#drop duplicates
df_retweet_users_edges = df_retweet_users_edges.drop_duplicates()
df_retweet_users_nodes = df_retweet_users_nodes.drop_duplicates()

df_retweet_users_edges.to_csv('rt_edges.csv',index=False)
df_retweet_users_nodes.to_csv('rt_nodes.csv',index=False)


# prepare data for gephi Mention Network T0D0
df_mention_edges = pd.DataFrame()
df_mention_nodes = pd.DataFrame()

# -

df_users_mentions.columns

input_h = "GiletJaune, giletjaune"
query = input_h.strip().replace(",", "+OR+")
print(query)

# # Conversation

# Similaire au retweet mais avec les user mentions. Qui parle à qui?

df_users_mentions;

# # OUTPUTS
#

##OUTPUT: Stats de bases. Quantifier le ‘bruit’
print("Number of tweets scraped in the current folder: " + str(len(df_tweets.index)))
print("Number of retweets: " + str(int(df_tweets['retweet_count'].sum())))
print("Number of favorite: " + str(int(df_tweets['favorite_count'].sum())))


# +
##OUTPUT: Who are the most influential accounts?

print('top retweeted accounts:')
print(top_influencers_rt_names)
print('top favorited accounts:')
print(top_influencers_fav_names)

# +
##OUTPUT: Stats de base: Hashtags les plus frequents
df_aggretated.columns
df_total_hashtag = df_aggretated.groupby('#').size().sort_values(0,ascending = False).reset_index()
df_total_hashtag.columns = ['#', 'count']
df_total_hashtag.head(30)

## T0D0 compute Jacquard coefficient
# -

##OUTPUT: INFO on the most favorited users
top_influencers_fav

##OUTPUT: INFO on the most retweeted users
top_influencers_rt

##OUTPUT: which users who retweet the most influential accounts?
who_rt.head(20)

##output: who are the influencers retweeted by an user, e.g. lexi82600? 
who_rt_who('lexi82600')

##OUTPUT: Get all tweets by username, eg GiletsJaunesFr
get_tweet_by_username('GiletsJaunesFr')


#output: top hashtags written to csv. you can also use function below
for name in top_influencers_rt_names:
    df_rel = get_related_hashtags_by_username(name)
    df_rel.to_csv('top_hashtags_by_'+name+'.csv',index=False)
    df_rel=[]

##OUTPUT: What hashtags do influencers use? Call function below with one of the names
get_related_hashtags_by_username('GiletsJaunesFr')


# ## GEPHI Output

df_users_mentions.head(1)

# # NLP

import spacy


# +
from tqdm import tqdm
import string
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
import concurrent.futures
import time
import pyLDAvis.sklearn
from pylab import bone, pcolor, colorbar, plot, show, rcParams, savefig
import warnings
warnings.filterwarnings('ignore')

# %matplotlib inline
import os

# Plotly based imports for visualization
from plotly import tools
import plotly.plotly as py
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.figure_factory as ff

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from spacy.lang.fr import French
import fr_core_news_sm
nlp = fr_core_news_sm.load()
# #!python -m spacy download fr_core_web_lg
# -

doc = nlp(df_tweets["text"][3])
spacy.displacy.render(doc, style='ent',jupyter=True)

punctuations = string.punctuation
stopwords = list(STOP_WORDS)

review = str(" ".join([i.lemma_ for i in doc]))

doc = nlp(review)
spacy.displacy.render(doc, style='ent',jupyter=True)

for i in nlp(review):
    print(i,"=>",i.pos_)

parser = French()
def spacy_tokenizer(sentence):
    mytokens = parser(sentence)
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    mytokens = [ word for word in mytokens if word not in stopwords and word not in punctuations ]
    mytokens = " ".join([i for i in mytokens])
    return mytokens


tqdm.pandas()
df_tweets["processed_text"] = df_tweets["text"].progress_apply(spacy_tokenizer)

tqdm.pandas()
df_users["processed_description"] = df_users["description"].progress_apply(spacy_tokenizer)

df_tweets.head(10)["processed_description"];

vectorizer = CountVectorizer(min_df=5, max_df=0.9, stop_words=stopwords, lowercase=True, token_pattern='[a-zA-Z\-][a-zA-Z\-]{2,}')
data_vectorized = vectorizer.fit_transform(df_tweets["processed_text"])

##How many topics do you want to find??
NUM_TOPICS = 3

lda = LatentDirichletAllocation(n_components=NUM_TOPICS, max_iter=10, learning_method='online',verbose=True)
data_lda = lda.fit_transform(data_vectorized)

# Non-Negative Matrix Factorization Model
nmf = NMF(n_components=NUM_TOPICS)
data_nmf = nmf.fit_transform(data_vectorized) 

# Latent Semantic Indexing Model using Truncated SVD
lsi = TruncatedSVD(n_components=NUM_TOPICS)
data_lsi = lsi.fit_transform(data_vectorized)


# Functions for printing keywords for each topic
def selected_topics(model, vectorizer, top_n=10):
    for idx, topic in enumerate(model.components_):
        print("Topic %d:" % (idx))
        print([(vectorizer.get_feature_names()[i], topic[i])
                        for i in topic.argsort()[:-top_n - 1:-1]]) 


print("LDA Model:")
selected_topics(lda, vectorizer)

# Keywords for topics clustered by Latent Semantic Indexing
print("NMF Model:")
selected_topics(nmf, vectorizer)

# Keywords for topics clustered by Non-Negative Matrix Factorization
print("LSI Model:")
selected_topics(lsi, vectorizer)

# Transforming an individual sentence
text = spacy_tokenizer("Les gilets jaune tous unis contre Macron. Tous dans la rue jusqu'à la démission")
x = lda.transform(vectorizer.transform([text]))[0]
print(x)

pyLDAvis.enable_notebook()
dash = pyLDAvis.sklearn.prepare(lda, data_vectorized, vectorizer, mds='tsne')
dash



df_tweets





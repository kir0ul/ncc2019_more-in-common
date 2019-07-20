# Python tools for analysis

Here you will find several scripts to load a tweets database, tracking certain hashtags, run an analysis and export your results. 


### Prerequisites

You will need python and jupyter notebook.

You will need to register an application at apps.twitter.com. Once you've created your application, note down the consumer key, consumer secret and then click to generate an access token and access token secret. With these four variables in hand you are ready to start using twarc.

We query Twitter's API to retrieve tweets and are hence limited by the query limitations. We use the twarc library which helps circumvents the rate limits. You will need to install it, more info on [twarc's github page](https://github.com/DocNow/twarc)

If you want to run some graph analysis, you will also need [networkx](https://networkx.github.io/documentation/stable/install.html)


### Getting data from Twitter (optional if you get your data another way like DMI-TCAT)

First we need to get a database of relevant tweets. 

You need to create a folder where you intend to store the tweets. The analysis will later run on an entire folder, so you could choose to create different folders for different hashtags, depending on your purpose. You can track one or multiple hashtags by separating them with commas. To track the hashtag "kusanagi" for example, run

```
python populate_hashtag.py #kusanagi folder_name
```

Note that you need to add the hashtag, otherwise you would also retrieve tweets containing the word kusanagi. 


To track and store tweets related to a certain hashtag as they are tweeted, run

```
python track_hashtag.py #kusanagai folder_name
```

Let's move on to the analysis.

## Analysing Data

### Reading json tweets

If you collected tweets with the above method, your tweets will be JSON formatted. Run the following to convert them into multiple tables (users, tweets, mentions, retweets, hashtags) in csv format.

```
python read_json_tweets.py json_folder csv_folder
```

### Getting statistics from data

Given csv_folder which contains csv outputted from the previous section, a general request will typically look like:

```
python aggregate.py csv_folder request
```
The following requests are available:

* rt_users: informations about users who were most retweeted
* fav_users: informations about users who were most favorited
* gen_stats: general statistics table
* top_hashtags: hashtags occurence table

There is also a more specific query available which looks like

```
python query_input.py csv_folder request input
```

Available requests are:

* tweet_by: get all tweets tweeted by 'input'
* related_hash_by: get all hashtags related to hashtag 'input'

### Graph Analysis (under construction)





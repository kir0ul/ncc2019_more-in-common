# Python tools for analysis

Here you will find several scripts to load a tweets database, tracking certain hashtags, run an analysis and export your results. 


### Prerequisites

You will need python and jupyter notebook.

We query Twitter's API to retrieve tweets and are hence limited by the query limitations. We use the twarc library which helps circumvents the rate limits. You will need to install it, more info on [twarc's github page](https://github.com/DocNow/twarc)

You will need to register an application at apps.twitter.com. Once you've created your application, note down the consumer key, consumer secret and then click to generate an access token and access token secret. With these four variables in hand you are ready to start using twarc.

### Setting up the databases

First we need to get a database of relevant tweets. 

You need to create a folder where you intend to store the tweets. The analysis will run on an entire folder, so you could create different folders for different hashtags, depending on your purpose. Then, to track the hashtag "kusanagi" for example, run

```
python populate_hashtag.py #kusanagi folder_name
```

Note that you need to add the hashtag, otherwise you would also retrieve tweets containing the word kusanagi. 


To track and store tweets related to a certain hashtag as they are tweeted, run

```
python track_hashtag.py #kusanagai folder_name
```

Let's move on to the analysis.

## Running analysis

For now, the analysis needs to be run inside the notebook load_and_explore.ipynb. The results can be shown in the outputs section. The section also outputs csv which can be exported into Gephi.

The analysis runs on:

### Gephi and Graph Analysis



# More in Common

+ *Thème :* citoyenneté.
+ *Phase d'avancement actuelle :* conception.
+ *Compétences associés :* data science, scrapping, vision produit.

## Résultats obtenus lors de la Nuit du Code Citoyen
Cette section contiendra les travaux effectué par l'équipe à la fin de la Nuit du Code Citoyen.

## Présentation de More in Common
+ More in Common est une organisation internationale à but non lucratif fondée en 2017.
  Elle a pour mission l’immunisation de nos sociétés contre la tentation du repli identitaire, social et culturel.
  En redonnant le goût de l’évidence à ce que les français ont en commun,
  More in Common œuvre à bâtir une société plus unie, accueillante et inclusive. 
+ More in Common mène des enquêtes d’opinion inédites dont l’objectif est de cartographier
  l’opinion des français sur l’ensemble des sujets qui divisent notre société aujourd’hui.
  Par leur ampleur et leur méthodologie [issus de la recherche en psychologie sociale],
  ces études sont désormais reconnues comme l’un des outils les plus innovants pour comprendre
  l’opinion publique et dépasser la polarisation croissante de nos sociétés. 
+ En effet, ces enquêtes n’ont pas simplement pour vocation de dresser un état des lieux:
  elles sont au service d’une stratégie. Elles ouvrent des voies pour rassembler,
  convaincre et mobiliser la société civile et tous les sans-voix, en faisant émerger un imaginaire partagé. 

En savoir plus : [moreincommon.com](https://www.moreincommon.com/).

## Problématique
+ Afin de bâtir une société plus unifiée, More in Common doit mettre fin aux divisions
  idéologiques et politiques qui minent la société française.
  Pour ce faire, elle doit comprendre l’origine de ces divisions:
  quels sujets divisent et pourquoi, et qui sont les instigateurs principaux de ces divisions. 
+ La polarisation apparente de notre société est, en effet, le jeu d’une minorité de personnes,
  les extrêmes, ou les ‘wings’. Ces extrêmes font beaucoup de ‘bruit’,
  notamment via les médias, et entretiennent des discours polarisants et une confrontation incessante,
  ce qui donne l’impression d’une société divisée dans son ensemble.
+ Mais la majorité des français est en réalité silencieuse et absente du débat public.
  C’est ce que nous appelons le _milieu ambivalent_:
  Une majorité délaissée et vulnérable aux discours identitaires et nationalistes,
  et pourtant plus modérée et ouverte aux compromis.
  Elle présente donc une opportunité pour engager un dialogue pacificateur et unificateur à l’échelle nationale. 

Nous souhaitons donner une voix et des opportunités d’expression aux français du _milieu ambivalent_.
Pour ce faire, nous devons en premier lieu délimiter un cadre d’expression et identifier les terrains de dialogue vacants.
Il s’agit donc d’identifier:
+	Les sujets clivants sur lesquels ils n’ont pas de voix mais doivent pouvoir s’exprimer
+	Le positionnement des ‘extrêmes’ sur ces grands sujets
+	Les influencers principaux qui sont à la source du ‘bruit’ sur des sujets donnés 

Comme projet pilote, nous aimerions tenter de délimiter puis créer des espaces de dialogue via les réseaux sociaux, et en particulier Twitter. D’où le défi qui suit…

# Tools for analysis

Here you will find several scripts to load a tweets database, tracking certain hashtags, run an analysis and export your results. 

## Prerequisites

You will need Python, Pip and jupyter notebook.

You will need to register an application at apps.twitter.com.
Once you've created your application, note down the consumer key, consumer secret
and then click to generate an access token and access token secret.
With these four variables in hand you are ready to start using twarc.

We query Twitter's API to retrieve tweets and are hence limited by the query limitations.
We use the [Twarc](https://github.com/DocNow/twarc) library which helps circumvents the rate limits.

If you want to run some graph analysis, you will also need [networkx](https://networkx.github.io/documentation/stable/install.html)

To install the project, run the following commands:
```
git clone https://gitlab.com/latitudes-exploring-tech-for-good/more-in-common/ncc2019_more-in-common.git
cd ncc2019_more-in-common
pip install pipenv
pipenv update
pipenv shell
```

## Quick start

Retrieve some tweets from `twitter` using the `Command Line Interface`:

```
python cli.py get "#TWITTER_HASHTAG_1,#TWITTER_HASHTAG_2" PATH_TO_SAVING_FOLDER
```

Example:
```
python cli.py get glyphosate data/glyphosate

```

Start the graphical interface (web page) to run some analysis on the data:
```
pipenv run python main.py
```

Now you can access the user interface in your browser: `http://127.0.0.1:8050/`

## Command line interface

A command line interface is available. You can get the help with:
```
python cli.py --help
```
Which yields:
```
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get    Get tweets from Twitter according to the specified HASHTAGS.
  query  Query on already saved data
  read   Read already saved tweets from IMPORT_FOLDER and export them to...
  stats  Compute statistics on already saved data
```

### Getting data from Twitter (optional if you get your data another way like DMI-TCAT)

First we need to get a database of relevant tweets:
- The analysis will run on an entire folder, so you could choose to create different folders for different hashtags, depending on your purpose.
- You can track one or multiple hashtags by separating them with commas.

Search for existing tweets:
```
python cli.py --method populate "#TWITTER_HASHTAG_1,#TWITTER_HASHTAG_2" PATH_TO_SAVING_FOLDER
```

Track tweets related to a certain hashtag as they are tweeted from now on:
```
python cli.py --method track "#TWITTER_HASHTAG_1,#TWITTER_HASHTAG_2" PATH_TO_SAVING_FOLDER
```

**Note that you need to add the hashtag, otherwise you would also retrieve tweets containing the hashtag you chose.**

You can get the help with the following command:
```
python cli.py get --help
```
Which yields:
```
Usage: cli.py get [OPTIONS] HASHTAGS PATH

  Get tweets from Twitter according to the specified HASHTAGS. Save them in
  JSON format in the specified PATH

Options:
  --method [populate|track]  Use 'populate' to get already existing tweets or
                             'track' to get new tweets published from now on
  --help                     Show this message and exit.
```

Let's move on to the analysis.

### Analysing Data

#### Converting raw tweets

This steps convert raw tweets collected with the above method into multiple tables (users, tweets, mentions, retweets, hashtags) in `csv` format:
```
python cli.py read IMPORT_FOLDER EXPORT_FOLDER
```

Example:
```
python cli.py read data/glyphosate data/glyphosate/CSV

```

You can get the help with the following command:
```
python cli.py read --help
```
Which yields:
```
Usage: cli.py read [OPTIONS] IMPORT_FOLDER EXPORT_FOLDER

  Read already saved tweets from IMPORT_FOLDER and export them to
  EXPORT_FOLDER as CSV tables

Options:
  --help  Show this message and exit.
```

#### Getting statistics from data

Given `TWEET_CSV_FOLDER` being the path to the folder which contains CSV files outputted
from the previous section:

**Genral statistics:**

The following requests are available:

* `rt_users`: informations about users who were most retweeted
* `fav_users`: informations about users who were most favorited
* `gen_stats`: general statistics table
* `top_hashtags`: hashtags occurence table

```
python cli.py stats TWEET_CSV_FOLDER --infos rt_users
```

Example:
```
python cli.py stats data/glyphosate/CSV --infos rt_users

```

You can get the help with the following command:
```
python cli.py stats --help
```
Which yields:
```
Usage: cli.py stats [OPTIONS] TWEET_CSV_FOLDER

  Compute statistics on already saved data

Options:
  --option [rt_users|fav_users|gen_stats|top_hashtags]
                                  Type of statistics to compute
  --help                          Show this message and exit.
```


**Specific queries:**

Available options are:
* `tweet_by`: get all tweets tweeted by 'input'
* `related_hash_by`: get all hashtags related to hashtag 'input'


```
python cli.py query --option QUERY_OPTION TWEET_CSV_FOLDER INPUT_TO_SEARCH
```

You can get the help with the following command:
```
python cli.py query --help
```
Which yields:
```
Usage: cli.py query [OPTIONS] TWEET_FOLDER QUERY

  Query on already saved data

Options:
  --option [get_tweet_by|get_related_hash_by]
                                  Type of statistics to compute
  --help                          Show this message and exit.
```
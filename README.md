# More in Common

+ *Thème :* citoyenneté.
+ *Phase d'avancement actuelle :* conception.
+ *Compétences associés :* data science, scrapping, vision produit.

## Résultats obtenus lors de la Nuit du Code Citoyen
Cette section contiendra les travaux effectué par l'équipe à la fin de la Nuit du Code Citoyen.

## Présentation de More in Common
+ More in Common est une organisation internationale à but non lucratif fondée en 2017. Elle a pour mission l’immunisation de nos sociétés contre la tentation du repli identitaire, social et culturel. En redonnant le goût de l’évidence à ce que les français ont en commun, More in Common œuvre à bâtir une société plus unie, accueillante et inclusive. 
+ More in Common mène des enquêtes d’opinion inédites dont l’objectif est de cartographier l’opinion des français sur l’ensemble des sujets qui divisent notre société aujourd’hui. Par leur ampleur et leur méthodologie [issus de la recherche en psychologie sociale], ces études sont désormais reconnues comme l’un des outils les plus innovants pour comprendre l’opinion publique et dépasser la polarisation croissante de nos sociétés. 
+ En effet, ces enquêtes n’ont pas simplement pour vocation de dresser un état des lieux : elles sont au service d’une stratégie. Elles ouvrent des voies pour rassembler, convaincre et mobiliser la société civile et tous les sans-voix, en faisant émerger un imaginaire partagé. 

En savoir plus : [moreincommon.com](https://www.moreincommon.com/).

## Problématique
+ Afin de bâtir une société plus unifiée, More in Common doit mettre fin aux divisions idéologiques et politiques qui minent la société française. Pour ce faire, elle doit comprendre l’origine de ces divisions : quels sujets divisent et pourquoi, et qui sont les instigateurs principaux de ces divisions. 
+ La polarisation apparente de notre société est, en effet, le jeu d’une minorité de personnes, les extrêmes, ou les ‘wings’. Ces extrêmes font beaucoup de ‘bruit’, notamment via les médias, et entretiennent des discours polarisants et une confrontation incessante, ce qui donne l’impression d’une société divisée dans son ensemble.
+ Mais la majorité des français est en réalité silencieuse et absente du débat public. C’est ce que nous appelons le ‘milieu ambivalent’ : Une majorité délaissée et vulnérable aux discours identitaires et nationalistes, et pourtant plus modérée et ouverte aux compromis. Elle présente donc une opportunité pour engager un dialogue pacificateur et unificateur à l’échelle nationale. 

Nous souhaitons donner une voix et des opportunités d’expression aux français du ‘milieu ambivalent’. Pour ce faire, nous devons en premier lieu délimiter un cadre d’expression et identifier les terrains de dialogue vacants. Il s’agit donc d’identifier… 
+	Les sujets clivants sur lesquels ils n’ont pas de voix mais doivent pouvoir s’exprimer
+	Le positionnement des ‘extrêmes’ sur ces grands sujets
+	Les influencers principaux qui sont à la source du ‘bruit’ sur des sujets donnés 

Comme projet pilote, nous aimerions tenter de délimiter puis créer des espaces de dialogue via les réseaux sociaux, et en particulier Twitter. D’où le défi qui suit…

## Tools for analysis

Here you will find several scripts to load a tweets database, tracking certain hashtags, run an analysis and export your results. 


### Prerequisites

You will need Python, Pip and jupyter notebook.

You will need to register an application at apps.twitter.com. Once you've created your application, note down the consumer key, consumer secret and then click to generate an access token and access token secret. With these four variables in hand you are ready to start using twarc.

We query Twitter's API to retrieve tweets and are hence limited by the query limitations. We use the twarc library which helps circumvents the rate limits. You will need to install it, more info on [twarc's github page](https://github.com/DocNow/twarc)

If you want to run some graph analysis, you will also need [networkx](https://networkx.github.io/documentation/stable/install.html)

To install the project, run the following commands:
```
git clone https://gitlab.com/latitudes-exploring-tech-for-good/more-in-common/ncc2019_more-in-common.git
cd ncc2019_more-in-common
pip install pipenv
pipenv update
pipenv shell
```

### Getting data from Twitter (optional if you get your data another way like DMI-TCAT)

First we need to get a database of relevant tweets.
The analysis will run on an entire folder, so you could choose to create different folders for different hashtags, depending on your purpose.
You can track one or multiple hashtags by separating them with commas.
```
python main.py --method populate --hashtags "#TWITTER_HASHTAG_1,#TWITTER_HASHTAG_2" --path PATH_TO_SAVING_FOLDER
```

To track and store tweets related to a certain hashtag as they are tweeted from now on, run:
```
python main.py --method track --hashtags "#TWITTER_HASHTAG_1,#TWITTER_HASHTAG_2" --path PATH_TO_SAVING_FOLDER
```

**Note that you need to add the hashtag, otherwise you would also retrieve tweets containing the hashtag you chose.**

In any case, you can get the help with:
```
python main.py --help
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


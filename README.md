# More in Common

+ *Thème :* citoyenneté.
+ *Phase d'avancement actuelle :* conception.
+ *Compétences associés :* data science, scrapping, vision produit.

##### #0 | Résultats obtenus lors de la Nuit du Code Citoyen
Cette section contiendra les travaux effectué par l'équipe à la fin de la Nuit du Code Citoyen.

##### #1 | Présentation de More in Common
+ More in Common est une organisation internationale à but non lucratif fondée en 2017. Elle a pour mission l’immunisation de nos sociétés contre la tentation du repli identitaire, social et culturel. En redonnant le goût de l’évidence à ce que les français ont en commun, More in Common œuvre à bâtir une société plus unie, accueillante et inclusive. 
+ More in Common mène des enquêtes d’opinion inédites dont l’objectif est de cartographier l’opinion des français sur l’ensemble des sujets qui divisent notre société aujourd’hui. Par leur ampleur et leur méthodologie [issus de la recherche en psychologie sociale], ces études sont désormais reconnues comme l’un des outils les plus innovants pour comprendre l’opinion publique et dépasser la polarisation croissante de nos sociétés. 
+ En effet, ces enquêtes n’ont pas simplement pour vocation de dresser un état des lieux : elles sont au service d’une stratégie. Elles ouvrent des voies pour rassembler, convaincre et mobiliser la société civile et tous les sans-voix, en faisant émerger un imaginaire partagé. 

En savoir plus : [moreincommon.com](https://www.moreincommon.com/).

##### #2 | Problématique
+ Afin de bâtir une société plus unifiée, More in Common doit mettre fin aux divisions idéologiques et politiques qui minent la société française. Pour ce faire, elle doit comprendre l’origine de ces divisions : quels sujets divisent et pourquoi, et qui sont les instigateurs principaux de ces divisions. 
+ La polarisation apparente de notre société est, en effet, le jeu d’une minorité de personnes, les extrêmes, ou les ‘wings’. Ces extrêmes font beaucoup de ‘bruit’, notamment via les médias, et entretiennent des discours polarisants et une confrontation incessante, ce qui donne l’impression d’une société divisée dans son ensemble.
+ Mais la majorité des français est en réalité silencieuse et absente du débat public. C’est ce que nous appelons le ‘milieu ambivalent’ : Une majorité délaissée et vulnérable aux discours identitaires et nationalistes, et pourtant plus modérée et ouverte aux compromis. Elle présente donc une opportunité pour engager un dialogue pacificateur et unificateur à l’échelle nationale. 

Nous souhaitons donner une voix et des opportunités d’expression aux français du ‘milieu ambivalent’. Pour ce faire, nous devons en premier lieu délimiter un cadre d’expression et identifier les terrains de dialogue vacants. Il s’agit donc d’identifier… 
+	Les sujets clivants sur lesquels ils n’ont pas de voix mais doivent pouvoir s’exprimer
+	Le positionnement des ‘extrêmes’ sur ces grands sujets
+	Les influencers principaux qui sont à la source du ‘bruit’ sur des sujets donnés 

Comme projet pilote, nous aimerions tenter de délimiter puis créer des espaces de dialogue via les réseaux sociaux, et en particulier Twitter. D’où le défi qui suit…

##### #3 | Le défi proposé

Développer un outil de lecture du ‘bruit’ sur Twitter : pour un hashtag (un thème) donné et que nous (More in Common) choisirions (input), il s’agirait d’identifier quels influencers & médias sont instigateurs de ce bruit et quels sujets sont associés à ce # de façon dominante, sur une période de temps définie.

##### #4 | Livrables
Des livrables en 2 étapes permettant de comprendre l’origine (qui et quoi) du bruit sur Twitter, à une période donnée et pour un thème (#) donné.

Important – ces ‘instructions’ ne sont ni limitantes, ni exhaustives. Si toutefois vous avez de meilleures idées pour rendre cet outil encore plus intéressant/performant, veuillez laisser libre cours à votre imagination ! 

1/ Création d’une base de données de tweets pour un input# donné
+ Créer un outil qui permette de générer et d’alimenter une base de données de tweets (en gardant le maximum d’informations sur chaque tweet, i.e. l’auteur, le nombre de likes, le nombre de commentaires, hashtags associés etc…).
+ Cet outil/script prendrait en entrée un hashtag et irait requêter (grâce à L’API de Twitter) tous les tweets concernés par ce hashtag sur une période de 7 jours maximum (contrainte imposée par Twitter) afin d’alimenter une base. 

2/ Créer une application permettant de requêter et de visualiser les caractéristiques de publication associées à l’input (#)

Inputs : L’utilisateur de l’application choisirait un hashtag  et une plage de date

Outputs : Extraction et visualisation des résultats :
+ Sujets dominants – identifier les sous-sujets dominants associés à l’input#. (bonus : analyser le contenu/texte (NLP) pour identifier des sous-thèmes plus précis, avec potentiellement une analyse de sentiment et style de rhétorique)
+ Statistiques de base : Nombre de posts , de likes, de retweets … associés à l’input# 
+ Influencers (comptes)  - Identifier les influencers principaux postant avec ce input# (ceux avec les posts les plus retweetés, les plus likés, le plus grand nombre de followers, nombre de publications, lange…)
+ Médias influents - identifier les médias les plus influents dans l’activité lié à l’input#. Analyser les liens postés provenant de sites de médias.
+ Visualisation des 100 tops tweets associés à l’input# afin que MIC puisse en faire une lecture qualitative – identifier si oui ou non il s’agit d’un sujet clivant. 

##### #5 | Ressources à disposition pour résoudre le défi
Pour vous approprier le projet, vous aurez accès aux ressources suivantes :
+ La présentation du projet ci-dessus
+ Mon aide et mon support !
+ La charte graphique de More in Common
+ L’API de tweeter (il suffit d’avoir un compte Tweeter pour y avoir accès gratuitement) : https://developer.twitter.com/en/docs.html

##### #6 | Code de conduite et philosophie du hackathon
Lors de la conception du hackathon, Latitudes a voulu prendre des partis-pris afin de rendre celui-ci particulier. 

Il s’agit d’éléments que nous souhaitons incarner collectivement avec vous tout au long des 24h :
+ La force du collectif pour faire émerger des solutions adaptées aux porteur.se.s de projets, notamment via la session de peer-learning ;
+ Une attention portée à la conception rapide, au test et à l’itération qui doivent permettre aux porteur.se.s de projets d’avoir accès aux solutions les plus abouties possibles ;
+ Le transfert de méthodes et postures, qui pourront être appliquées et transmises aux équipes par les animateur.trice.s, les mentors ET les autres équipes ;
+ L’engagement sur des solutions ouvertes, facilement utilisables par les porteur.se.s de projets, et qui vous permettront de continuer à contribuer à l’issue du hackathon si vous le souhaitez, ou de permettre à d’autres personnes de le faire.

##### #7 | Points de contact lors du hackathon
+ Lucie : membre de More in Common et porteuse de projets.
+ Margot : bénévole Latitudes, et en charge de la préparation du défi avec More in Common.
+ Yannick : co-fondateur de Latitudes.

##### #8 | Setup du back-end

```
cd back
pip install pipenv
pipenv install
pipenv shell
FLASK_ENV=development FLASK_APP=app.py flask run --host=0.0.0.0
```
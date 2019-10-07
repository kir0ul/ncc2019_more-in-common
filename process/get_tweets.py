import sys
import datetime
import traceback
import os
from twarc import Twarc
import json


language = "fr"

#### /!\ REQUIRED: input your credentials here
consumer_key = "4ha4rLgP6Ci6fEZtaqttGTKoA"
consumer_secret = "5ckLaCgfTdfmWM7qS9f2w05pDCSIWRCTHlm7RLnKwK9tCWIz9P"
access_token = "602145669-jHmxtsl0wSZDFeZxi81GcTzYrD87dRBhF78ip0qo"
access_token_secret = "YFLMmVVdcN4gb4KDX3MeOjbjxoKnnsFvjKxjRGMkkEZ5D"


def main(get_method=None, input_hashtags=None, storage_location=None):
    if not os.path.exists(storage_location):
        os.makedirs(storage_location, exist_ok=True)

    hashtag_query = input_hashtags.strip().replace(",", "+OR+")

    try:
        tweets = 0
        t = Twarc(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret,
            tweet_mode="extended",
        )

        print(
            "Started storing tweets related to "
            + input_hashtags
            + " at "
            + storage_location
            + " since "
            + str(datetime.datetime.now())
        )

        if get_method == "populate":
            for tweet in t.search(hashtag_query, lang=language):
                with open(
                    os.path.join(
                        storage_location, "tweet" + str(tweet["id"]) + ".json"
                    ),
                    "w",
                    encoding="utf8",
                ) as file:
                    json.dump(tweet, file)
                    tweets += 1

        elif get_method == "track":
            for tweet in t.filter(hashtag_query):
                with open(
                    storage_location, "/tweet" + str(tweet["id"]) + ".json",
                    "w",
                    encoding="utf8",
                ) as file:
                    json.dump(tweet, file)
                    tweets += 1
        else:
            print("No method defined, exiting...")

    except KeyboardInterrupt:
        print("Shutdown requested...successfully stored " + str(tweets) + " tweets")
    except BaseException:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)

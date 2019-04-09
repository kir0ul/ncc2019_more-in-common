from twarc import Twarc
import json
import sys
import datetime

input_hashtag = sys.argv[1]
storage_location = sys.argv[2]

#### /!\ REQUIRED: input your credentials here
consumer_key = '4ha4rLgP6Ci6fEZtaqttGTKoA'
consumer_secret = '5ckLaCgfTdfmWM7qS9f2w05pDCSIWRCTHlm7RLnKwK9tCWIz9P'
access_token = '602145669-jHmxtsl0wSZDFeZxi81GcTzYrD87dRBhF78ip0qo'
access_token_secret = 'YFLMmVVdcN4gb4KDX3MeOjbjxoKnnsFvjKxjRGMkkEZ5D'


def main():

	try:
		tweets = 0
		t = Twarc(consumer_key, consumer_secret, access_token, access_token_secret,tweet_mode= 'extended')

		print("Started storing tweets related to "+ input_hashtag + " at " + storage_location + " since " + str(datetime.datetime.now()))
		for tweet in t.filter(input_hashtag):
			with open(storage_location + '/tweet'+str(tweet['id'])+'.json', 'w', encoding='utf8') as file:
				json.dump(tweet, file)
				tweets += 1

	except KeyboardInterrupt:
		print("Shutdown requested...successfully stored " + str(tweets) + " tweets")
	except Exception:
		traceback.print_exc(file=sys.stdout)
	sys.exit(0)

if __name__ == '__main__':
	main()
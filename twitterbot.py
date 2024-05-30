import time
import tweepy

bearer_token = r""
api_key = ""
api_secret = ""
access_token = ""
access_token_secret = ""
client_id = ""
client_id_secret = ""


client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


# Bot's unique ID
client_id = client.get_me().data.id



# client.create_tweet(text="Using X api")
# client.like("1787927326421831764")
client.retweet()
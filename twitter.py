import tweepy as tw
import credential
import certifi
from pymongo import MongoClient


auth = tw.OAuthHandler(credential.API_key, credential.API_secretkey)
auth.set_access_token(credential.Access_token, credential.Accesss_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

tweets = api.user_timeline(screen_name="@ani_thomas_", count=100, include_rts=False, tweet_mode='extended')
Twitter = []
for info in tweets:
    status = {
        "ID": str(info.id), "TweetAuthor": info.author.name,
        "TweetText": info.full_text, "DateandTime": info.created_at.strftime("%b %d %Y %H:%M:%S"),
        "TweetSource": info.source
    }
    Twitter.append(status)
client = MongoClient("mongodb+srv://Ani:WeatherCan@cluster0.i5fm0.mongodb.net/SocialMedia?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["SocialMedia"]
collection = db["Twitter"]
collection.insert_many(Twitter)
print(Twitter)
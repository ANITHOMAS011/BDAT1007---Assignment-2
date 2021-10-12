import pip
import praw
import datetime as dt
import credential
import certifi
from pymongo import MongoClient

redditAuth = praw.Reddit(client_id=credential.Client_ID, client_secret=credential.Client_SecretID, user_agent=credential.user_agent,
                         username=credential.username, password=credential.Password)

Reddit = []
for post in redditAuth.redditor(credential.username).submissions.top():
    redditPosts = {
        "PostId": post.id,
        "PostAuthor": post.author.name,
        "PostTitle": post.title,
        "PostText": post.selftext,
        "DateandTime": dt.datetime.fromtimestamp(post.created).strftime("%b %d %Y %H:%M:%S"),
        }
    Reddit.append(redditPosts)
client = MongoClient("mongodb+srv://Ani:WeatherCan@cluster0.i5fm0.mongodb.net/SocialMedia?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["SocialMedia"]
collection = db["Reddit"]
collection.insert_many(Reddit)

print(Reddit)
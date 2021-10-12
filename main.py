from flask import Flask, request, render_template
from pymongo import MongoClient
import credential
import datetime as dt
import praw
import certifi
import tweepy as tw

app = Flask(__name__)

#Mongodb connection
client = MongoClient("mongodb+srv://Ani:WeatherCan@cluster0.i5fm0.mongodb.net/SocialMedia?ssl=true&ssl_cert_reqs=CERT_NONE")
db= client["SocialMedia"]

# reddit authentication
redditAuth = praw.Reddit(client_id=credential.Client_ID, client_secret=credential.Client_SecretID, user_agent=credential.user_agent,
                         username=credential.username, password=credential.Password)
# twitter authentication
auth = tw.OAuthHandler(credential.API_key, credential.API_secretkey)
auth.set_access_token(credential.Access_token, credential.Accesss_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Reddit')
def Reddit():
    return render_template("Reddit.html")

@app.route('/redditPost', methods=['POST'])
def redditPost():
    title = request.values.get("title")
    status = request.values.get("status")
    sub = redditAuth.subreddit("socialdatamining")
    update = sub.submit(title, status)
    collection = db.Reddit
    collection.insert_one({
        "PostId": update.id,
        "PostAuthor": update.author.name,
        "PostTitle": update.title,
        "PostText": update.selftext,
        "Dateandtime": dt.datetime.fromtimestamp(update.created).strftime("%b %d %Y %H:%M:%S"),
    })
    return render_template('home.html')

@app.route('/Twitter')
def Twitter():
    return render_template("Twitter.html")

@app.route('/twitterPost', methods=['POST'])
def twitterPost():
    tweet = request.values.get("status")
    update = api.update_status(tweet)
    collection = db.Twitter
    collection.insert_one({
        "ID": str(update.id),
        "TweetAuthor": update.author.name,
        "TweetText": update.text,
        "DateandTime": update.created_at.strftime("%b %d %Y %H:%M:%S"),
        "TweetSource": update.source
    })
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, g, redirect, render_template, session
from twitter_provider import XApiAuthHandler, XApiProvider
from form import TweetSearchForm, AccountConnectionStatusForm

# TODO - implement TwitterParser to info similar to API (follows, likes, retweets)
# TODO - implement tweets publication (based on pre-generated URL)
# TODO - implement tweet search by user

load_dotenv()
# Below data is available via X Developer Profile
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_API_SECRET = os.environ.get("CONSUMER_API_SECRET")
# This shall be specified anew in X Developer Profile
CALLBACK_URL = (
    "https://5464-2a06-c701-7253-3300-dc2d-a9aa-9ab9-286f.ngrok-free.app/callback"
)
# This is for Flask only
APP_SECRET = os.environ.get("INTERNAL_APP_SECRET")

app = Flask(__name__)
app.secret_key = APP_SECRET
twitter_auth_handler = XApiAuthHandler(
    consumer_api_key=CONSUMER_API_KEY,
    consumer_api_secret=CONSUMER_API_SECRET,
    callback_url=CALLBACK_URL,
)
twitter_provider = XApiProvider()


@app.before_request
def before_request():
    g.twitter_auth_handler = twitter_auth_handler
    g.twitter_provider = twitter_provider


@app.route("/")
def home():
    print(CLIENT_SECRET)
    auth_handler = g.twitter_auth_handler
    auth_url = auth_handler.get_user_auth_url()
    return render_template("index.html", auth_url=auth_url)


@app.route("/callback")
def callback_url():
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")
    auth_handler = g.twitter_auth_handler
    try:
        access_token, access_token_secret = auth_handler.get_user_auth_data(
            oauth_verifier
        )
        res = {
            "oauth_token": oauth_token,
            "oauth_verifier": oauth_verifier,
            "access_token": access_token,
            "access_token_secret": access_token_secret,
        }
        session["access_token"] = access_token
        session["token_secret"] = access_token_secret
        return render_template("authed.html", res=res)
    except Exception as e:
        logging.warning(str(e))
        return redirect("/")


@app.route("/tweet/<current_username>", methods=["GET", "POST"])
def tweet_lookup(current_username):
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    twitter_provider: XApiProvider = g.twitter_provider
    if not access_token or not token_secret:
        return redirect("/")
    tweet_form = TweetSearchForm(request.form)
    liked = False
    retweeted = False
    if tweet_form.validate_on_submit():
        tweet_id = tweet_form.tweet_id.data
        liking_usernames = twitter_provider.get_tweet_likes(
            tweet_id=tweet_id,
            consumer_key=CONSUMER_API_KEY,
            consumer_secret=CONSUMER_API_SECRET,
            access_token=access_token,
            access_token_secret=token_secret,
        )
        if current_username in liking_usernames:
            liked = True
        retweeters_usernames = twitter_provider.get_tweet_retweets(
            tweet_id=tweet_id,
            consumer_key=CONSUMER_API_KEY,
            consumer_secret=CONSUMER_API_SECRET,
            access_token=access_token,
            access_token_secret=token_secret,
        )
        if current_username in retweeters_usernames:
            retweeted = True
    return render_template(
        "form.html",
        is_tweet=True,
        form=tweet_form,
        current_username=current_username,
        liked=liked,
        retweeted=retweeted,
    )


@app.route("/follow/<current_username>", methods=["GET", "POST"])
def user_lookup(current_username):
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    twitter_provider: XApiProvider = g.twitter_provider
    if not access_token or not token_secret:
        return redirect("/")
    user_form = AccountConnectionStatusForm(request.form)
    connection_status = None
    username = None
    if user_form.validate_on_submit():
        username = user_form.username.data
        connection_status = twitter_provider.get_connection_status(
            username=username,
            consumer_key=CONSUMER_API_KEY,
            consumer_secret=CONSUMER_API_SECRET,
            access_token=access_token,
            access_token_secret=token_secret,
        )
    return render_template(
        "form.html",
        is_tweet=False,
        form=user_form,
        connection_status=connection_status,
        current_username=current_username,
    )


@app.route("/info")
def info():
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    if not access_token or not token_secret:
        return redirect("/")
    twitter_provider: XApiProvider = g.twitter_provider
    res_info = twitter_provider.get_user_info(
        consumer_key=CONSUMER_API_KEY,
        consumer_secret=CONSUMER_API_SECRET,
        access_token=access_token,
        access_token_secret=token_secret,
    )
    return render_template("info.html", res_info=res_info)


if __name__ == "__main__":
    app.run(debug=True)

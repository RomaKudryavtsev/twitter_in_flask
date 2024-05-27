import os
import logging
from flask import Flask, request, g, redirect, render_template, session
from twitter_provider import TwitterAuthHandler, TwitterApiProvider

# Below data is available via X Developer Profile
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
CONSUMER_API_SECRET = os.environ.get("CONSUMER_API_SECRET")
# This shall be specified anew in X Developer Profile
CALLBACK_URL = (
    "https://503c-2a00-a041-789f-ba00-d462-8835-6a89-fe8f.ngrok-free.app/callback"
)
# This is for Flask only
APP_SECRET = os.environ.get("INTERNAL_APP_SECRET")

app = Flask(__name__)
app.secret_key = APP_SECRET
twitter_auth_handler = TwitterAuthHandler(
    consumer_api_key=CONSUMER_API_KEY,
    consumer_api_secret=CONSUMER_API_SECRET,
    callback_url=CALLBACK_URL,
)


@app.before_request
def before_request():
    g.twitter_auth_handler = twitter_auth_handler
    g.twitter_provider = TwitterApiProvider()


@app.route("/")
def home():
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


@app.route("/info")
def info():
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    if not access_token or not token_secret:
        return redirect("/")
    twitter_provider: TwitterApiProvider = g.twitter_provider
    res_info = twitter_provider.get_user_info(
        consumer_key=CONSUMER_API_KEY,
        consumer_secret=CONSUMER_API_SECRET,
        access_token=access_token,
        access_token_secret=token_secret,
    )
    return render_template("info.html", res_info=res_info)


if __name__ == "__main__":
    app.run(debug=True)

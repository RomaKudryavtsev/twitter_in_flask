import logging
import traceback
from flask import Blueprint, g, request, session, render_template, redirect
from tweepy import TweepyException
from config import config
from twitter_provider import XApiAuthHandler, XApiProvider, ClientApiProvider
from form import TweetSearchForm, UserConnectionStatusForm, CheckTweetForm

x_api_bp = Blueprint("x_api", __name__)


@x_api_bp.route("/")
def home():
    x_auth_handler = g.x_auth_handler
    try:
        auth_url = x_auth_handler.get_user_auth_url()
    except TweepyException:
        g.x_auth_handler = XApiAuthHandler(
            consumer_api_key=config.CONSUMER_API_KEY,
            consumer_api_secret=config.CONSUMER_API_SECRET,
            callback_url=config.CALLBACK_URL,
        )
        auth_url = x_auth_handler.get_user_auth_url()
        redirect("/")
    return render_template("index.html", auth_url=auth_url)


@x_api_bp.route("/callback")
def callback_url():
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")
    x_auth_handler = g.x_auth_handler
    try:
        access_token, access_token_secret = x_auth_handler.get_user_auth_data(
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
        logging.warning(traceback.format_exc())
        logging.warning(str(e))
        return redirect("/")


@x_api_bp.route("/info")
def info():
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    if not access_token or not token_secret:
        return redirect("/")
    x_api_provider: XApiProvider = g.x_api_provider
    client_api_provider: ClientApiProvider = g.client_api_provider
    res_info = x_api_provider.get_user_me(
        access_token=access_token,
        access_token_secret=token_secret,
    )
    banner_url = client_api_provider.get_user_info_by_screen_name(
        screen_name=res_info["username"]
    )["banner_url"]
    return render_template("info.html", res_info=res_info, banner_url=banner_url)


@x_api_bp.route("/search/<current_username>", methods=["GET", "POST"])
def search_tweet(current_username):
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    x_api_provider: XApiProvider = g.x_api_provider
    if not access_token or not token_secret:
        return redirect("/")
    tweet_count = int(request.args.get("tweet_count"))
    tweet_form = CheckTweetForm(request.form)
    published = False
    if tweet_form.validate_on_submit():
        search_text = tweet_form.search_text.data
        user_id = x_api_provider.get_user_me(
            access_token=access_token, access_token_secret=token_secret
        )["id"]
        found_tweets = x_api_provider.search_user_tweets(
            user_id=user_id,
            search_text=search_text,
            access_token=access_token,
            access_token_secret=token_secret,
            count=tweet_count,
        )
        if found_tweets:
            published = True
    return render_template(
        "form.html",
        is_tweet=False,
        is_client_api=False,
        is_intent=False,
        is_search=True,
        form=tweet_form,
        current_username=current_username,
        published=published,
        tweet_count=tweet_count,
    )


@x_api_bp.route("/tweet/<current_username>", methods=["GET", "POST"])
def tweet_lookup(current_username):
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    x_api_provider: XApiProvider = g.x_api_provider
    if not access_token or not token_secret:
        return redirect("/")
    tweet_form = TweetSearchForm(request.form)
    liked = False
    retweeted = False
    if tweet_form.validate_on_submit():
        tweet_id = tweet_form.tweet_id.data
        liking_usernames = x_api_provider.get_tweet_likes(
            tweet_id=tweet_id,
            access_token=access_token,
            access_token_secret=token_secret,
        )
        liked = current_username in liking_usernames
        retweeters_usernames = x_api_provider.get_tweet_retweets(
            tweet_id=tweet_id,
            access_token=access_token,
            access_token_secret=token_secret,
        )
        retweeted = current_username in retweeters_usernames
    return render_template(
        "form.html",
        is_tweet=True,
        is_clinet_api=False,
        is_intent=False,
        is_search=False,
        form=tweet_form,
        current_username=current_username,
        liked=liked,
        retweeted=retweeted,
    )


@x_api_bp.route("/follow/<current_username>", methods=["GET", "POST"])
def user_lookup(current_username):
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    x_api_provider: XApiProvider = g.x_api_provider
    if not access_token or not token_secret:
        return redirect("/")
    user_form = UserConnectionStatusForm(request.form)
    connection_status = None
    username = None
    if user_form.validate_on_submit():
        username = user_form.username.data
        connection_status = x_api_provider.get_connection_status(
            username=username,
            access_token=access_token,
            access_token_secret=token_secret,
        )
    return render_template(
        "form.html",
        is_tweet=False,
        is_client_api=False,
        is_intent=False,
        is_search=False,
        form=user_form,
        connection_status=connection_status,
        current_username=current_username,
    )

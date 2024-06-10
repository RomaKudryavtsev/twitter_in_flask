import logging
import traceback
from flask import Blueprint, g, request, render_template, abort
from twitter_provider import ClientAPIProviderManager
from form import TweetSearchForm, UserConnectionStatusForm, CheckTweetForm

client_api_bp = Blueprint("client_api", __name__, url_prefix="/client_api")


def get_user_id(client_manager, current_username):
    return client_manager.execute_w_retry(
        "get_user_info_by_screen_name", screen_name=current_username
    )["id"]


@client_api_bp.route("/search/<current_username>", methods=["GET", "POST"])
def search_tweet(current_username):
    client_manager: ClientAPIProviderManager = g.client_api_manager
    tweet_form = CheckTweetForm(request.form)
    tweet_count = int(request.args.get("tweet_count"))
    found_tweets = []
    if tweet_form.validate_on_submit():
        search_text = tweet_form.search_text.data
        user_id = get_user_id(client_manager, current_username)
        try:
            found_tweets = client_manager.execute_w_retry(
                "search_user_tweets",
                search_text=search_text,
                user_id=user_id,
                count=tweet_count,
            )
        except RuntimeError as e:
            logging.error(e)
            logging.warning(traceback.format_exc())
            abort(400)
    return render_template(
        "form.html",
        is_tweet=False,
        is_search=True,
        is_client_api=True,
        is_intent=False,
        form=tweet_form,
        found_tweets=found_tweets,
        current_username=current_username,
        tweet_count=tweet_count,
    )


@client_api_bp.route("/tweet/<current_username>", methods=["GET", "POST"])
def tweet_lookup(current_username):
    tweet_count = int(request.args.get("tweet_count"))
    client_manager: ClientAPIProviderManager = g.client_api_manager
    tweet_form = TweetSearchForm(request.form)
    liked = False
    retweeted = False
    if tweet_form.validate_on_submit():
        tweet_id = tweet_form.tweet_id.data
        user_id = get_user_id(client_manager, current_username)
        try:
            user_likes = client_manager.execute_w_retry(
                "get_user_likes",
                count=tweet_count,
                user_id=user_id,
            )
            liked = str(tweet_id) in user_likes
            user_retweets = client_manager.execute_w_retry(
                "get_user_retweets",
                count=tweet_count,
                user_id=user_id,
            )
            retweeted = str(tweet_id) in user_retweets
        except RuntimeError as e:
            logging.error(e)
            logging.warning(traceback.format_exc())
            abort(400)
    return render_template(
        "form.html",
        is_tweet=True,
        is_search=False,
        is_client_api=True,
        is_intent=False,
        form=tweet_form,
        current_username=current_username,
        liked=liked,
        retweeted=retweeted,
        tweet_count=tweet_count,
    )


@client_api_bp.route("/follow/<current_username>", methods=["GET", "POST"])
def user_lookup(current_username):
    following_count = int(request.args.get("following_count"))
    client_manager: ClientAPIProviderManager = g.client_api_manager
    user_form = UserConnectionStatusForm(request.form)
    connection_status = False
    if user_form.validate_on_submit():
        target_username = user_form.username.data
        try:
            following = client_manager.execute_w_retry(
                "get_user_following",
                count=following_count,
                current_screen_name=current_username,
            )
            connection_status = target_username in following
        except RuntimeError as e:
            logging.error(e)
            logging.warning(traceback.format_exc())
            abort(400)
    return render_template(
        "form.html",
        is_tweet=False,
        is_search=False,
        is_client_api=True,
        is_intent=False,
        form=user_form,
        connection_status=str(connection_status),
        current_username=current_username,
        following_count=following_count,
    )

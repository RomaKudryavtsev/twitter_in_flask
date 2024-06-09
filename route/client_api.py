from flask import Blueprint, g, request, render_template
from twitter_provider import ClientApiProvider
from form import TweetSearchForm, UserConnectionStatusForm, CheckTweetForm

client_api_bp = Blueprint("client_api", __name__, url_prefix="/client_api")


@client_api_bp.route("/search/<current_username>", methods=["GET", "POST"])
def search_tweet(current_username):
    client_api_provider: ClientApiProvider = g.client_api_provider
    tweet_form = CheckTweetForm(request.form)
    tweet_count = int(request.args.get("tweet_count"))
    found_tweets = []
    if tweet_form.validate_on_submit():
        search_text = tweet_form.search_text.data
        user_id = client_api_provider.get_user_info_by_screen_name(
            screen_name=current_username
        )["id"]
        found_tweets = client_api_provider.search_user_tweets(
            search_text=search_text, user_id=user_id, count=tweet_count
        )
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
    client_api_provider: ClientApiProvider = g.client_api_provider
    tweet_form = TweetSearchForm(request.form)
    liked = False
    retweeted = False
    if tweet_form.validate_on_submit():
        tweet_id = tweet_form.tweet_id.data
        user_id = client_api_provider.get_user_info_by_screen_name(
            screen_name=current_username
        )["id"]
        user_likes = client_api_provider.get_user_likes(
            count=tweet_count,
            user_id=user_id,
        )
        liked = str(tweet_id) in user_likes
        user_retweets = client_api_provider.get_user_retweets(
            count=tweet_count,
            user_id=user_id,
        )
        retweeted = str(tweet_id) in user_retweets
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
    client_api_provider: ClientApiProvider = g.client_api_provider
    user_form = UserConnectionStatusForm(request.form)
    connection_status = False
    if user_form.validate_on_submit():
        target_username = user_form.username.data
        following = client_api_provider.get_user_following(
            count=following_count,
            current_screen_name=current_username,
        )
        connection_status = target_username in following
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

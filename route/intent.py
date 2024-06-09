from flask import Blueprint, request, session, render_template, redirect
from form import TwitterIntentForm
from twitter_provider import WebIntentProvider

intent_bp = Blueprint("intent", __name__, url_prefix="/intent")
X_LOGIN_URL = "https://x.com/i/flow/login"


@intent_bp.route("/<current_username>", methods=["GET", "POST"])
def post_intent(current_username):
    access_token = session.get("access_token")
    token_secret = session.get("token_secret")
    if not access_token or not token_secret:
        return redirect("/")
    intent_form = TwitterIntentForm(request.form)
    intent_url = ""
    if intent_form.validate_on_submit():
        text = intent_form.text.data
        intent_url = WebIntentProvider.get_tweet_intent_url(text=text)
    return render_template(
        "form.html",
        is_tweet=False,
        is_intent=True,
        is_search=False,
        intent_url=intent_url,
        x_login_url=X_LOGIN_URL,
        form=intent_form,
        current_username=current_username,
    )

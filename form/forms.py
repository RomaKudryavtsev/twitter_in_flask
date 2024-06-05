from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class TweetSearchForm(FlaskForm):
    tweet_id = IntegerField("Tweet ID", validators=[DataRequired()])
    submit = SubmitField("Check Likes & Retweets by Authed User")


class AccountConnectionStatusForm(FlaskForm):
    username = StringField("Target Username", validators=[DataRequired()])
    submit = SubmitField("Check Target User's Status with Authed User")

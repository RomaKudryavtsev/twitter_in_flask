from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class TweetSearchForm(FlaskForm):
    tweet_id = IntegerField("Tweet ID", validators=[DataRequired()])
    submit = SubmitField("Check Likes & Retweets by Authed User")


class UserConnectionStatusForm(FlaskForm):
    username = StringField("Target Username", validators=[DataRequired()])
    submit = SubmitField("Check Target User's Status with Authed User")


# For cases without X API Auth
class ClientAPITweetForm(FlaskForm):
    tweet_id = IntegerField("Tweet ID", validators=[DataRequired()])
    username = StringField("Target Username", validators=[DataRequired()])
    submit = SubmitField("Check Likes & Retweets by the Target User")


# For cases without X API Auth
class ClientAPIFollowForm(FlaskForm):
    current_username = StringField("Current Username", validators=[DataRequired()])
    target_username = StringField("Target Username", validators=[DataRequired()])
    submit = SubmitField("Check if the Current User follows the Target User")

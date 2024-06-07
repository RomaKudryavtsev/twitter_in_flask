from flask import Blueprint, g
from config import config
from twitter_provider import ClientApiProvider

client_api_bp = Blueprint("client_api", __name__, url_prefix="/client_api")
client_api_provider = ClientApiProvider(
    screen_name=config.SCREEN_NAME,
    screen_pwd=config.SCREEN_PWD,
)


@client_api_bp.before_request
def before_request():
    g.client_provider = client_api_provider

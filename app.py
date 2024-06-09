from flask import Flask, g
from config import config
from route import x_api_bp, client_api_bp, intent_bp
from twitter_provider import XApiAuthHandler, XApiProvider, ClientApiProvider

# TODO - implement tweet search by user
# TODO - add banner img retrieval

app = Flask(__name__)
app.secret_key = config.APP_SECRET
app.static_folder = "./static"
app.register_blueprint(x_api_bp)
app.register_blueprint(client_api_bp)
app.register_blueprint(intent_bp)

x_auth_handler = XApiAuthHandler(
    consumer_api_key=config.CONSUMER_API_KEY,
    consumer_api_secret=config.CONSUMER_API_SECRET,
    callback_url=config.CALLBACK_URL,
)
x_api_provider = XApiProvider(
    consumer_key=config.CONSUMER_API_KEY,
    consumer_secret=config.CONSUMER_API_SECRET,
)
client_api_provider = ClientApiProvider(
    screen_name=config.SCREEN_NAME,
    screen_pwd=config.SCREEN_PWD,
)


@app.before_request
def before_request():
    g.x_auth_handler = x_auth_handler
    g.x_api_provider = x_api_provider
    g.client_api_provider = client_api_provider


if __name__ == "__main__":
    app.run(debug=True)

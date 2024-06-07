from flask import Flask
from config import config
from route import x_api_bp, client_api_bp

# TODO - implement tweets publication (based on pre-generated URL)
# TODO - implement tweet search by user

app = Flask(__name__)
app.secret_key = config.APP_SECRET
app.register_blueprint(x_api_bp)
app.register_blueprint(client_api_bp)

if __name__ == "__main__":
    app.run(debug=True)

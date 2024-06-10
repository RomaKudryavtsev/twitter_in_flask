# twitter_manager_py

Flask App demonstrating:
1) X's 3-legged OAuth authentication with Flask
2) Usage of X API and Twitter Client API (via a number of provider instances)
3) Usage of Web Intents

## Configuration Steps
- Create new project and app via X Developer Portal.
- Get your *CONSUMER_API_KEY* and *CONSUMER_API_SECRET* - those are refferring to the **developer's** account.
- Turn on OAuth 1.0 under the User authentication settings section of your app’s Settings tab. **NB**: Active DNS-record and local ngrok tunnel are required.
- After enabling OAuth 1.0, get your *CLIENT_ID* and *CLIENT_SECRET* - those are also refferring to the **developer's** account.
- Specify callback url (based on the ngrok tunnel url in app.py).

## Authentication Process
- When user visits home page, **TwitterAuthHandler** will provide an active authentication url to X UI.
- User visits the url and authorizes the app to read data from his X Account.
- User is redirected to the app's callback url. At this moment the app receives in request params *oauth_token* and *oauth_verifier*. Based on these, **TwitterAuthHandler** will collect the **user's** *access_token* and *access_secret*, which can be stored for further requests to X API (in the example they are stored in Flask's session).
- Based on the **user's** *access_token* and *access_secret*, **TwitterApiProvider** is able to retrieve data via X API.

## Running locally
1) Create file *provider_workers.csv* in project root with screen names, passwords, proxy IP and proxy ports for Client API.

*Example:* `x_screen_name,x_screen_pwd,proxy_ip,proxy_port`

2) Run `python app.py`

*NB:* After project first start - *cookie_<screen_name>.json* files will be created in root directory (theses files are responsible for storing cookies for Client API providers sessions)
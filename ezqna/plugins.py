import os
from flask_migrate import Migrate
from flask_login import LoginManager, current_user as original_current_user
from authlib.integrations.flask_client import OAuth

from ezqna.models import User, db

migrate = Migrate(db=db)
login_manager = LoginManager()
current_user: User = original_current_user  # type: ignore
oauth = OAuth()
oauth.register(
    name="twitter",
    api_base_url="https://api.twitter.com/1.1/",
    request_token_url="https://api.twitter.com/oauth/request_token",
    access_token_url="https://api.twitter.com/oauth/access_token",
    authorize_url="https://api.twitter.com/oauth/authenticate",
    client_id=os.getenv("TWITTER_CLIENT_ID"),
    client_secret=os.getenv("TWITTER_CLIENT_SECRET"),
    # fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
)

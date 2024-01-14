from flask import Blueprint, redirect, url_for
from flask_login import login_user, logout_user

from ezqna.plugins import oauth
from ezqna.models import db, User
from ezqna.utils import get_config

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/login")
def login():
    redirect_uri = url_for("auth.verify", _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)  # type: ignore


@bp.get("/verify")
def verify():
    token = oauth.twitter.authorize_access_token()  # type: ignore
    url = "account/verify_credentials.json"
    resp = oauth.twitter.get(url, params={"skip_status": True})  # type: ignore
    user_data = resp.json()

    user = db.session.query(User).where(User.id == token["user_id"]).one_or_none()
    if not user:
        user = User(
            id=token["user_id"],
            name=user_data["name"],
            username=token["screen_name"],
            token=token["oauth_token"],
            token_secret=token["oauth_token_secret"],
            avatar=user_data["profile_image_url_https"],
            is_admin=False,
        )
    else:
        user.name = user_data["name"]
        user.username = token["screen_name"]
        user.token = token["oauth_token"]
        user.token_secret = token["oauth_token_secret"]
        user.avatar = user_data["profile_image_url_https"]

    if user.id == get_config("ADMIN_TWITTER_ID"):
        user.is_admin = True

    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect("/")


@bp.get("/logout")
def logout():
    logout_user()
    return redirect("/")

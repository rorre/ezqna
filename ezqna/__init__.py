from os import environ
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import select


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
        "DATABASE_URI", "sqlite:///project.db"
    )
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

    from ezqna.plugins import migrate, login_manager, oauth
    from ezqna.models import db, User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.execute(
            select(User).filter(User.username == user_id)
        ).scalar_one_or_none()

    oauth.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    from ezqna.routes.index import bp as index_bp
    from ezqna.routes.auth import bp as auth_bp
    from ezqna.routes.question import bp as question_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(question_bp)

    return app

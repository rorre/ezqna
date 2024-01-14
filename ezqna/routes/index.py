from flask import Blueprint, url_for
from flask_login import current_user, login_required

import liku as e
from liku.integrations.flask import component

from ezqna.components.base import Layout
from ezqna.components.index import QuestionBox, QuestionForm
from ezqna.models import Question, db

bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("/")
@component
def home():
    return Layout(
        e.div(
            props={"class_": "flex flex-col m-4"},
            children=[
                QuestionForm(current_user.is_authenticated),
                e.div(
                    props={
                        "class_": "flex flex-col gap-4",
                        "id": "questions",
                        "hx-trigger": "load, updated",
                        "hx-get": url_for("question.questions"),
                    }
                ),
            ],
        )
    )


@bp.get("/profile")
@login_required
@component
def my_questions():
    questions = db.session.query(Question).where(Question.user == current_user)
    return Layout(
        e.div(
            props={"class_": "flex flex-col m-4"},
            children=[QuestionBox(q, False) for q in questions],
        )
    )

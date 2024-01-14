from flask import Blueprint
from ezqna.components.index import QuestionBox
from ezqna.dto import AnswerQuestion, CreateQuestion
from ezqna.utils import validate
from ezqna.models import db, Question
from ezqna.plugins import current_user
import liku as e
from liku.integrations.flask import component

bp = Blueprint("question", __name__, url_prefix="/questions")


@bp.post("/answer/<int:question_id>")
@validate
def answer_question(question_id: int, form: AnswerQuestion):
    if not (current_user.is_authenticated and current_user.is_admin):
        return "forbidden", 403

    question = (
        db.session.query(Question).where(Question.id == question_id).one_or_none()
    )
    if not question:
        return "not found", 404

    question.answer = form.answer
    db.session.add(question)
    db.session.commit()
    return "ok"


@bp.post("/submit")
@validate
def submit_question(form: CreateQuestion):
    q = Question(question=form.question)
    if not form.anonymous and current_user.is_authenticated:
        q.user_id = current_user.id
        q.user = current_user

    db.session.add(q)
    db.session.commit()
    return "ok"


@bp.get("/")
@component
def questions():
    is_admin = current_user.is_authenticated and current_user.is_admin
    questions = db.session.query(Question)
    if not is_admin:
        questions = questions.where(Question.answer.is_not(None))
    return e.Fragment(children=[QuestionBox(q, is_admin) for q in questions])

from typing import Literal
import liku as e
from flask import url_for

from ezqna.models import Question
from ezqna.utils import get_config


def QuestionForm(is_authenticated: bool):
    return e.form(
        props={
            "class_": "rounded-box bg-base-200 flex flex-col gap-4 px-8 py-8",
            "hx-post": url_for("question.submit_question"),
            "hx-on::after-request": "this.reset()",
            "hx-swap": "none",
        },
        children=[
            e.strong(
                props={"class_": "text-3xl"},
                children=f"Got a question for {get_config('USER')}?",
            ),
            e.textarea(
                props={
                    "class_": "textarea textarea-bordered w-full mt-4",
                    "type": "text",
                    "placeholder": "Your question here",
                    "name": "question",
                    "minlength": 1,
                    "maxlength": "280",
                }
            ),
            e.div(
                props={
                    "class_": "flex flex-col md:flex-row justify-between md:items-center gap-4",
                },
                children=[
                    e.div(
                        props={"class_": "inline-flex items-center gap-4"},
                        children=[
                            e.input(
                                props={
                                    "type": "checkbox",
                                    "class_": "toggle",
                                    "name": "anonymous",
                                }
                            ),
                            e.p(children="Anonymous"),
                        ],
                    )
                    if is_authenticated
                    else e.a(
                        props={
                            "href": url_for("auth.login"),
                            "class_": "link link-hover",
                        },
                        children=f"Log in to let {get_config('USER')} know who you are!",
                    ),
                    e.button(
                        props={
                            "class_": "btn btn-primary",
                            "type": "submit",
                        },
                        children="Send",
                    ),
                ],
            ),
        ],
    )


def QuestionBox(question: Question, is_admin: bool):
    return e.div(
        props={"class_": "rounded-box bg-base-200 flex flex-col gap-4 px-8 py-8"},
        children=[
            ChatBubble(
                question.user.avatar
                if question.user
                else "https://ui-avatars.com/api/?name=Anonymous",
                question.user.name if question.user else "Anonymous",
                question.question,
                "start",
            ),
            ChatBubble(
                get_config("AVATAR"),
                get_config("USER"),
                question.answer,
                "end",
            )
            if question.answer
            else None,
            e.form(
                props={
                    "class_": "flex flex-col gap-4",
                    "hx-post": f"/questions/answer/{question.id}",
                    "hx-on::after-request": "htmx.trigger('#questions', 'updated')",
                    "hx-swap": "none",
                },
                children=[
                    e.textarea(
                        props={
                            "class_": "textarea textarea-bordered w-full mt-4",
                            "type": "text",
                            "placeholder": "Update your answer here"
                            if question.answer
                            else "Your answer here",
                            "name": "answer",
                            "minlength": 1,
                            "maxlength": "280",
                        }
                    ),
                    e.button(
                        props={
                            "class_": "btn btn-primary",
                            "type": "submit",
                        },
                        children="Send",
                    ),
                ],
            )
            if is_admin
            else None,
        ],
    )


def ChatBubble(
    avatar: str, username: str, content: str, position: Literal["start", "end"]
):
    return e.div(
        props={
            "class_": "chat " + ("chat-start" if position == "start" else "chat-end")
        },
        children=[
            e.div(
                props={"class_": "chat-image avatar"},
                children=e.div(
                    props={"class_": "w-10 rounded-full"},
                    children=e.img(props={"src": avatar}),
                ),
            ),
            e.div(props={"class_": "chat-header"}, children=username),
            e.div(
                props={"class_": "chat-bubble prose whitespace-pre-line"},
                children=content,
            ),
        ],
    )

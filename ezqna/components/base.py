from flask import url_for
import liku as e
from liku import HTMLElement

from ezqna.plugins import current_user


def Navbar():
    return e.nav(
        props={
            "class_": "flex flex-row px-4 py-2 items-center gap-4 justify-between m-4 bg-base-200 rounded-box"
        },
        children=[
            e.a(
                props={"href": "/"},
                children=e.strong(
                    props={"class_": "font-bold text-lg"}, children="EasyQnA"
                ),
            ),
            e.div(
                props={"class_": "flex flex-col md:flex-row gap-4 md:items-center"},
                children=[
                    e.a(
                        props={"href": "/auth/login", "class_": "btn btn-primary"},
                        children="Login",
                    )
                    if not current_user.is_authenticated
                    else e.details(
                        props={"class_": "dropdown dropdown-end"},
                        children=[
                            e.summary(
                                props={"class_": "btn btn-circle"},
                                children=e.img(
                                    props={
                                        "src": current_user.avatar,
                                        "class_": "rounded-full w-10 h-10",
                                    }
                                ),
                            ),
                            e.ul(
                                props={
                                    "class_": "mt-1 p-2 shadow menu dropdown-content z-[1] bg-base-200 rounded-box w-52"
                                },
                                children=[
                                    e.li(
                                        children=e.a(
                                            props={"href": "/profile"},
                                            children="My questions",
                                        )
                                    ),
                                    e.li(
                                        children=e.a(
                                            props={"href": "/auth/logout"},
                                            children="Logout",
                                        )
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def Layout(children: HTMLElement):
    return e.html(
        children=[
            e.head(
                children=[
                    e.meta(props={"charset": "UTF-8"}),
                    e.meta(
                        props={
                            "name": "viewport",
                            "content": "width=device-width, initial-scale=1.0",
                        }
                    ),
                    e.title(children="EasyQnA"),
                    e.link(
                        props={
                            "href": url_for("static", filename="style.css"),
                            "rel": "stylesheet",
                            "type": "text/css",
                        }
                    ),
                    e.script(props={"src": url_for("static", filename="htmx.min.js")}),
                ]
            ),
            e.main(
                props={"class_": "container mx-auto"},
                children=[Navbar(), children],
            ),
        ]
    )

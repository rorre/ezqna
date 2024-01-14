from functools import cache, wraps
import os
import typing as t
from flask import flash, jsonify, redirect, request
from pydantic import BaseModel, ValidationError

from werkzeug.datastructures import MultiDict

P = t.ParamSpec("P")
K = t.TypeVar("K")
V = t.TypeVar("V")
TResponse = t.TypeVar("TResponse")
ValidateModel = t.Type[BaseModel] | None


def multidict_to_dict(multidict: MultiDict[K, V]) -> dict[K, list[V] | V]:
    obj: dict[K, list[V] | V] = {}
    for key, val in multidict.lists():
        obj[key] = val
        if len(val) == 1:
            obj[key] = val[0]

    return obj


def validate(f: t.Callable[P, TResponse]):
    types = t.get_type_hints(f)
    form_model: ValidateModel = types.get("form")
    query_model: ValidateModel = types.get("query")
    json_model: ValidateModel = types.get("json")

    @wraps(f)
    def inner(*args: P.args, **kwargs: P.kwargs):
        try:
            if form_model:
                kwargs["form"] = form_model.model_validate(
                    multidict_to_dict(request.form)
                )

            if query_model:
                kwargs["query"] = query_model.model_validate(
                    multidict_to_dict(request.args)
                )

            if json_model:
                kwargs["json"] = json_model.model_validate_json(request.data)
        except ValidationError as e:
            errors = e.errors()
            best_mimetype = request.accept_mimetypes.best_match(
                ["application/json", "text/html"], "application/json"
            )
            if best_mimetype == "application/json":
                return jsonify(errors), 400

            print(errors)
            for error in errors:
                path = ".".join(map(str, error["loc"]))
                flash(f'{path}: {error["msg"]}', "error")
            return redirect(request.path)

        return f(*args, **kwargs)

    return inner


@cache
def get_config(name: str):
    return os.getenv(name, "")

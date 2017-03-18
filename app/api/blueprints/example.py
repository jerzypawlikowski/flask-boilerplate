#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from ..utlis.http import json_response

example_blueprint = Blueprint("example", __name__)


@example_blueprint.route("/", methods=["GET"])
def index():
    return json_response(
        status=200,
        response_data={
            "success": True,
            "data": {
                "articles": [
                    {"id": 1, "title": "hello world"},
                    {"id": 2, "title": "second example"}
                ]
            }
        }
    )

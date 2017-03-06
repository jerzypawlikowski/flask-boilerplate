#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

from ..utlis.http import json_response

hello_blueprint = Blueprint("hello", __name__)


@hello_blueprint.route("/", methods=["GET"])
def index():
    return json_response(
        status=200,
        response_data={
            "success": True,
            "data": "hello world"
        }
    )

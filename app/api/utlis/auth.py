#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import session

from app.api.models import User
from .http import json_response


def authenticate(func):
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return json_response(
                status=401, response_data={"success": False}
            )
        user = User.query.get(session["user_id"])
        return func(user, *args, **kwargs)
    return wrapped

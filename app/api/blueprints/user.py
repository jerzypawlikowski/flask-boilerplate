#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request, session
from jsonschema import ValidationError
from sqlalchemy.exc import IntegrityError

from app.api.models import User
from app.api.utlis.auth import authenticate
from app.api.utlis.http import json_response
from app.api.utlis.validators import validate_dict_with_schema

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("", methods=["GET"])
def list_users():
    """
    List all users of the system
    """
    return json_response(
        status=200,
        response_data={
            "success": True,
            "data": {
                "users": [user.serialize() for user in User.all()]
            }
        }
    )


@user_blueprint.route("register/", methods=["POST"])
def register():
    """
    Register a new user
    """
    try:
        request_data = json.loads(request.data)
        validate_dict_with_schema(request_data, "user/register/request")
        user = User(
            email=request_data["email"],
            password=User.create_hash(plain_password=request_data["password"])
        )
        user.save()
        return json_response(
            status=200,
            response_data={"success": True,  "data": {"user": user.serialize()}}
        )
    except (TypeError, ValueError):
        errors = ["Invalid JSON"]
    except ValidationError as e:
        errors = e.message
    except IntegrityError:
        errors = ["This email address is already registered"]

    if errors:
        return json_response(
            status=400, response_data={"success": False, "errors": errors}
        )


@user_blueprint.route("login/", methods=["POST"])
def login():
    """
    Log in the user
    """
    errors = None
    try:
        request_data = json.loads(request.data)
        validate_dict_with_schema(request_data, "user/register/request")
        user = User.check_user(
            email=request_data["email"],
            password=request_data["password"]
        )
        if user:
            session["user_id"] = user.id
            return json_response(
                status=200,
                response_data={
                    "success": True, "data": {"user": user.serialize()}
                }
            )
    except (TypeError, ValueError):
        errors = ["Invalid JSON"]
    except ValidationError as e:
        errors = e.message

    if errors:
        return json_response(
            status=400, response_data={"success": False, "errors": errors}
        )

    return json_response(
        status=401,
        response_data={"success": False, "errors": ["Invalid email/password"]}
    )


@user_blueprint.route("logout/", methods=["GET", "POST"])
def logout():
    """
    Log out the user
    """
    session.clear()
    return json_response(status=200, response_data={"success": True})


@user_blueprint.route("me/", methods=["GET"])
@authenticate
def me(user):
    """
    Get details of the current user
    """
    return json_response(
        status=200,
        response_data={"success": True, "data": {"user": user.serialize()}}
    )

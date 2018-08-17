#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from app.api.models import User
from app.api.utlis.validators import validate_dict_with_schema


def test_wrong_url(app):
    """
    Given the app is up and running
    When I make a call
    Then I get HTTP 404 NOT FOUND response
    """
    client = app.test_client()
    response = client.get("/api/wrong")
    assert response.status_code == 404


# TEST LISTING

def test_list_success(app, db):
    """
    Given I have two users in the database
    When I make a call to the `users` API
    Then I get HTTP 200 OK response
    And the response body match the schema
    And the response contains data for two users
    """
    for user in [
        User(email="a{}@example.com".format(n), password="a") for n in range(2)
    ]:
        user.save()

    client = app.test_client()
    response = client.get("/api/users/")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(
        response_data,
        "user/list/response"
    )
    assert len(response_data["data"]["users"]) == 2


def test_list_wrong_method(app):
    """
    Given the app is up and running
    But I use wrong HTTP method
    When I make a call
    Then I get HTTP 405 METHOD NOT ALLOWED response
    """
    client = app.test_client()
    response = client.post("/api/users/")
    assert response.status_code == 405


# TEST REGISTRATION

def test_register_success(app, db):
    """
    Given I provide valid email and password
    When I make a call to the `register` API
    Then I get HTTP 200 OK response
    And the response body match the schema
    And the response contains new user's data
    And the new user is in the db
    """
    data = {
        "email": "a@example.com",
        "password": "test123"
    }

    client = app.test_client()
    response = client.post("/api/users/register/", data=json.dumps(data))
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(
        response_data,
        "user/register/response"
    )
    assert response_data["data"]["user"]["email"] == data["email"]


def test_register_no_data(app):
    """
    Given I do not provide valid JSON
    When I make a call to the `register` API
    Then I get HTTP 400 BAD REQUEST response
    """
    client = app.test_client()
    response = client.post("/api/users/register/")
    assert response.status_code == 400


def test_register_existing_email(app, db):
    """
    Given I provide email that is already registered
    When I make a call to the `register` API
    Then I get HTTP 400 BAD REQUEST response
    """
    data = {
        "email": "a@example.com",
        "password": "test123"
    }
    user = User(**data)
    user.save()

    client = app.test_client()
    response = client.post("/api/users/register/", data=json.dumps(data))
    assert response.status_code == 400
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(response_data, "error_response")
    assert "This email address is already registered" in response_data["errors"]


def test_register_invalid_email(app):
    """
    Given I do not provide valid email
    When I make a call to the `register` API
    Then I get HTTP 400 BAD REQUEST response
    """
    data = {
        "email": "not-an-email",
        "password": "test123"
    }
    client = app.test_client()
    response = client.post("/api/users/register/", data=json.dumps(data))
    assert response.status_code == 400
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(response_data, "error_response")
    assert "'not-an-email' is not a 'email'" in response_data["errors"]


def test_register_short_password(app):
    """
    Given I do not provide valid password
    When I make a call to the `register` API
    Then I get HTTP 400 BAD REQUEST response
    """
    data = {
        "email": "a@example.com",
        "password": "test"
    }
    client = app.test_client()
    response = client.post("/api/users/register/", data=json.dumps(data))
    assert response.status_code == 400
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(response_data, "error_response")
    assert "'test' is too short" in response_data["errors"]


def test_register_wrong_method(app):
    """
    Given the app is up and running
    But I use wrong HTTP method
    When I make a call to `register` API
    Then I get HTTP 405 METHOD NOT ALLOWED response
    """
    client = app.test_client()
    response = client.get("/api/users/register/")
    assert response.status_code == 405


# TEST LOGIN

def test_login_success(app, db):
    """
    Given I provide valid email and password
    When I make a call to the `login` API
    Then I get HTTP 200 OK response
    And the response body match the schema
    And the response contains user's data
    """
    data = {
        "email": "a@example.com",
        "password": "test123"
    }
    User(
        email=data["email"],
        password=User.create_hash(plain_password=data["password"])
    ).save()

    client = app.test_client()
    response = client.post("/api/users/login/", data=json.dumps(data))
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(
        response_data,
        "user/register/response"
    )
    assert response_data["data"]["user"]["email"] == data["email"]


def test_login_not_existing(app, db):
    """
    Given I provide email that is not registered
    When I make a call to the `login` API
    Then I get HTTP 401 UNAUTHORIZED response
    """
    data = {
        "email": "a@example.com",
        "password": "test123"
    }

    client = app.test_client()
    response = client.post("/api/users/login/", data=json.dumps(data))
    assert response.status_code == 401
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(response_data, "error_response")
    assert "Invalid email/password" in response_data["errors"]


def test_login_wrong_password(app, db):
    """
    Given I provide email that is registered
    But I provide wrong password
    When I make a call to the `login` API
    Then I get HTTP 401 UNAUTHORIZED response
    """
    data = {
        "email": "a@example.com",
        "password": "test123"
    }

    client = app.test_client()
    response = client.post("/api/users/login/", data=json.dumps(data))
    assert response.status_code == 401
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(response_data, "error_response")
    assert "Invalid email/password" in response_data["errors"]


def test_login_wrong_data(app, db):
    """
    Given I don't provide data in a valid format
    When I make a call to the `login` API
    Then I get HTTP 400 BAD REQUEST response
    """
    client = app.test_client()
    response = client.post("/api/users/login/", data=json.dumps({}))
    assert response.status_code == 400
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(response_data, "error_response")


def test_login_no_data(app):
    """
    Given I do not provide valid JSON
    When I make a call to the `login` API
    Then I get HTTP 400 BAD REQUEST response
    """
    client = app.test_client()
    response = client.post("/api/users/login/")
    assert response.status_code == 400


def test_login_wrong_method(app):
    """
    Given the app is up and running
    But I use wrong HTTP method
    When I make a call to `login` API
    Then I get HTTP 405 METHOD NOT ALLOWED response
    """
    client = app.test_client()
    response = client.get("/api/users/login/")
    assert response.status_code == 405


# TEST LOGOUT


def test_logout_success(app):
    """
    Given that I am logged in
    When I make a call to `logout` API
    Then I get HTTP 200 OK response
    """
    client = app.test_client()
    response = client.post("/api/users/logout/")
    assert response.status_code == 200
    response_data = json.loads(response.data.decode("utf-8"))
    validate_dict_with_schema(
        response_data,
        "user/logout/response"
    )

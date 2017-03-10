#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from app.api.utlis.validators import validate_dict_with_schema


def test_hello(app):
    """
    Given the app is up and running
    When I make a call to the API
    Then I get HTTP 200 OK response
    And the response body match the schema
    """
    client = app.test_client()
    response = client.get("/api/hello/")
    assert response.status_code == 200
    validate_dict_with_schema(
        json.loads(response.data.decode("utf-8")),
        "hello/response"
    )


def test_wrong_url(app):
    """
    Given the app is up and running
    When I make a call
    Then I get HTTP 404 NOT FOUND response
    """
    client = app.test_client()
    response = client.get("/api/wrong")
    assert response.status_code == 404


def test_wrong_method(app):
    """
    Given the app is up and running
    But I use wrong HTTP method
    When I make a call
    Then I get HTTP 405 METHOD NOT ALLOWED response
    """
    client = app.test_client()
    response = client.post("/api/hello/")
    assert response.status_code == 405

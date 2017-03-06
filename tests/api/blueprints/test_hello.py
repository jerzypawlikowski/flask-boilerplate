#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_hello(app):
    """
    Given the app is up and running
    When I make a call to the API
    Then I get HTTP 200 OK response
    """
    client = app.test_client()
    response = client.get("/api/hello/")
    assert response.status_code == 200


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

#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_main(app):
    """
    Given the app is up and running
    When I make a call to the frontend page
    Then I get HTTP 200 OK response
    """
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

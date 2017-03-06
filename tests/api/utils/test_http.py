#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.api.utlis.http import json_response


def test_empty_response():
    """
    When I call`json_response` function without arguments
    Then I get HTTP 200 OK response
    And the response body is empty
    """
    response = json_response()
    assert response.status_code == 200
    assert response.data.decode("utf-8") == u""

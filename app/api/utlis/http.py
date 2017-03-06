#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Response


def json_response(status=200, response_data=None):
    """
    Returns HTTP response with JSON body
    """
    headers = {"Content-Type": "application/json"}

    if response_data is None:
        data = None
    else:
        data = json.dumps(response_data)

    return Response(status=status, response=data, headers=headers)

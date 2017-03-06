#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from app.factory import create_app


@pytest.fixture(scope="function")
def app(request):
    """
    Provides test application
    """
    application = create_app()

    # Establish an application context before running the tests.
    ctx = application.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return application

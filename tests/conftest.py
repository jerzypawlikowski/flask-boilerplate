#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from flask import g

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


@pytest.fixture(scope="function")
def db(app, request):
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    my_db = app.extensions["sqlalchemy"].db

    def teardown():
        import contextlib
        from sqlalchemy import MetaData

        engine = my_db.engine
        meta = MetaData(engine)
        meta.reflect()

        with contextlib.closing(engine.connect()) as con:
            trans = con.begin()
            for table in reversed(meta.sorted_tables):
                con.execute(table.delete())
            trans.commit()
        ctx.pop()

    request.addfinalizer(teardown)

    # Set this one as global db handler
    g.db = my_db

    return my_db

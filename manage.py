#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.factory import create_app

app = create_app()

if __name__ == "main":
    app.run()

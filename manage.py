#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager

from app.factory import create_app

app = create_app()


def main():
    manager = Manager(app=app)
    manager.run()

if __name__ == "__main__":
    main()

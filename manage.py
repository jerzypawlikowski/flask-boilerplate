#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager

from app.factory import create_app

app = create_app()


def main():
    manager = Manager(app=app)

    @manager.command
    def build_frontend():
        import os
        from subprocess import Popen
        node_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "app/static/js"
        )
        p = Popen("npm run build", cwd=node_directory, shell=True)
        p.wait()

    manager.run()

if __name__ == "__main__":
    main()

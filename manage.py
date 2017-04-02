#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from app.factory import create_app, db

app = create_app()


def main():
    directory = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")
    )

    Migrate(app, db, directory=directory)
    manager = Manager(app=app)
    manager.add_command("db", MigrateCommand)

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

    @manager.command
    def routes():
        from flask import url_for
        import urllib
        output = []
        for rule in app.url_map.iter_rules():

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ",".join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.parse.unquote(
                "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        for line in sorted(output):
            print(line)

    manager.run()

if __name__ == "__main__":
    main()

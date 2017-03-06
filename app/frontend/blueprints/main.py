#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

main_blueprint = Blueprint("main_blueprint", __name__)


@main_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from pip.req import parse_requirements


setup(
    name="flask-boilerplate",
    author="Jerzy Pawlikowski",
    version="1.0.0",
    py_modules=["app"],
    install_requires=parse_requirements("requirements.txt")
)

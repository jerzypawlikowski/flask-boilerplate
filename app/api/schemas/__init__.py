#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json


def load_schemas_from_directory(directory, schema=None):
    """
    Loads schemas from given directory and returns a dictionary
    """
    if not os.path.isdir(directory):
        raise ValueError("{} is not a directory".format(directory))

    for (directory_path, directories, files) in os.walk(directory):
        relative_path = os.path.relpath(directory_path, directory)
        current_schema = schema

        if relative_path not in (".", "__pycache__"):
            for part in relative_path.split("/"):
                current_schema = current_schema[part]

        for directory_name in directories:
            if directory_name not in current_schema:
                current_schema[directory_name] = {}

        for filename in filter(lambda name: name.endswith(".json"), files):
            schema_name = os.path.splitext(filename)[0]
            with open(os.path.join(directory_path, filename), "r") as fp:
                content = json.load(fp)
                current_schema[schema_name] = content
                fp.close()

    return schema

current_directory = os.path.dirname(os.path.abspath(__file__))

validation_schema = load_schemas_from_directory(
    current_directory,
    {
        "$schema": "http://json-schema.org/schema#",
        "id": "#"
    }
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonschema import (
    Draft4Validator, FormatChecker, RefResolver, ValidationError
)

from app.api.schemas import validation_schema


def validate_dict_with_schema(dictionary, schema_path):
    """
    Validates a dictionary against a schema with given `schema_path`
    """
    validator = Draft4Validator(
        validation_schema,
        resolver=RefResolver.from_schema(validation_schema),
        format_checker=FormatChecker()
    )
    schema = validation_schema
    for path_part in schema_path.split('/'):
        schema = schema[path_part]
    errors = [
        error.message for error in validator.iter_errors(dictionary, schema)
        ]
    if errors:
        raise ValidationError(errors)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.event import listen

from app.factory import db


class BaseModel(db.Model):
    """
    Base model with `created_at` and `updated_at` fields
    """
    __abstract__ = True
    fields_to_serialize = []

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        return cls.query.all()

    def serialize(self, fields=None):
        serialized = {}
        for field in fields or self.fields_to_serialize:
            field_value = getattr(self, field)
            if isinstance(field_value, datetime):
                field_value = field_value.isoformat()
            serialized[field] = field_value

        return serialized


def set_updated_at(target, value, oldvalue):
    """
    Set updated_at value
    """
    value.updated_at = datetime.now()


listen(BaseModel, "before_update", set_updated_at)

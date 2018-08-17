#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bcrypt
from sqlalchemy.exc import SQLAlchemyError

from app.api.utlis.models import BaseModel
from app.factory import db


class User(BaseModel):
    """
    Class representing a user of the system
    """
    __tablename__ = "users"
    fields_to_serialize = ["id", "email"]

    id = db.Column(db.BigInteger, primary_key=True)

    email = db.Column(db.String(254), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    @classmethod
    def create_hash(cls, plain_password: str) -> str:
        """
        Hashes plain password
        """
        return bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        """
        Check if the password is correct
        """
        return bcrypt.hashpw(
            plain_password.encode("utf-8"),
            self.password.encode("utf-8")
        ).decode("utf-8") == self.password

    @staticmethod
    def check_user(email: str, password: str) -> None:
        """
        Check if email and password matches an existing user
        """
        try:
            user = User.query.filter_by(email=email.lower()).one()
            if user.check_password(plain_password=password):
                return user
        except (SQLAlchemyError, ValueError):
            return None

# -*- coding: utf-8 -*-
from mongoengine import Document, fields

from tests.models.user import User


class Post(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.ObjectIdField(required=True)


class PostWithReference(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.ReferenceField(User, required=True)

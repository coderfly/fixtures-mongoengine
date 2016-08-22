# -*- coding: utf-8 -*-
import datetime
from mongoengine import Document, fields

from tests.models.user import User


class Post(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.ReferenceField(User, required=True)


class PostWithAuthorId(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.ObjectIdField(required=True)

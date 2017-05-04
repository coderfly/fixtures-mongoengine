# -*- coding: utf-8 -*-
from mongoengine import Document, fields, EmbeddedDocument

from tests.models.user import User


class Post(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.ObjectIdField(required=True)
    created_at = fields.DateTimeField()


class PostWithReference(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.ReferenceField(User, required=True)
    created_at = fields.DateTimeField()


class AuthorEmbedded(EmbeddedDocument):
    id = fields.ObjectIdField(required=True)
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=True)


class PostWithEmbedded(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    author = fields.EmbeddedDocumentField(AuthorEmbedded, required=True)
    created_at = fields.DateTimeField()


class PostWithList(Document):
    title = fields.StringField(required=True)
    text = fields.StringField(required=True)
    authors = fields.ListField(fields.EmbeddedDocumentField(AuthorEmbedded, required=True))
    created_at = fields.DateTimeField()

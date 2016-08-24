# -*- coding: utf-8 -*-

from mongoengine import Document, fields


class Circular(Document):
    name = fields.StringField(required=True)

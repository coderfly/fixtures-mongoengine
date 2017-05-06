# -*- coding: utf-8 -*-

from mongoengine import Document, fields


class Simple(Document):
    name = fields.StringField(required=True)

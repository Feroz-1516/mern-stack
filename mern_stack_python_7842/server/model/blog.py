from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime

class Blog(Document):
    title = StringField(required=True)
    desc = StringField(required=True)
    img = StringField(required=True)
    user = ReferenceField('User', required=True)
    date = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'blogs'
    }
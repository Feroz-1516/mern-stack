from mongoengine import Document, StringField, EmailField, ListField, ReferenceField

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
    blogs = ListField(ReferenceField('Blog'), required=True)

    meta = {
        'collection': 'users'
    }
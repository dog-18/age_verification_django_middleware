from peewee import *

# Django's middleware is not allowed to have models in the same way normal apps are.
# (At least I couldn't find a way how to do it).
# We have to manage our own database to store the tokens.
db = SqliteDatabase('age_verification_tokens.db')

class TokenDB(Model):
    uuid = CharField(unique=True)
    expiration_unixtime = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([TokenDB])

# TODO: the db is currently not pruned from expired tokens.
from django.db import models
from uuid import uuid4
from datetime import date
import json

# Create your models here.
class Poll(models.Model):
    name = models.TextField()
    choices = models.TextField()
    uuid = models.TextField()
    creation_date = models.DateTimeField()

def NewPoll(name, choices, uuid=None, creation_date=None):
    if uuid is None:
        uuid = uuid4()
    if creation_date is None:
        creation_date = date.today().isoformat()
    str_choices = json.dumps(choices)
    return Poll(
        name = name,
        choices = str_choices,
        uuid = uuid,
        creation_date = creation_date
    )

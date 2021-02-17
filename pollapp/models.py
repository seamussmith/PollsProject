from typing import Type
from django.db import models
from uuid import uuid4
from datetime import date
import json


# Create your models here.
# ? Maybe make an abstract class with these implmentations?

class Poll(models.Model):
    name = models.TextField()
    uuid = models.TextField(primary_key=True)
    def get_choices(uuid):
        raise NotImplementedError()

class Choice(models.Model):
    question = models.TextField()
    votes = models.IntegerField()
    uuid = models.TextField(primary_key=True)
    poll_uuid = models.TextField()
    @staticmethod
    def new(question, poll_uuid):
        return Choice(
            question = question,
            poll_uuid = poll_uuid,
            uuid = str(uuid4()),
            votes = 0
        )

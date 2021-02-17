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
    @staticmethod
    def new(name, questions):
        new_uuid = str(uuid4())
        for question in questions:
            choice = Choice.new(question, new_uuid)
            choice.save()
        return Poll(
            name = name,
            uuid = new_uuid
        )
    def get_choices(self):
        return Choice.objects.get(uuid=self.uuid)
    def to_dict(self):
        choices = [i.to_dict() for i in Choice.objects.all() if i.poll_uuid == self.uuid]
        return {
            "name": self.name,
            "uuid": self.uuid,
            "choices": choices
        }

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
    def to_dict(self):
        return {
            "question": self.question,
            "votes": self.votes,
            "uuid": self.uuid,
            "poll_uuid": self.poll_uuid,
        }

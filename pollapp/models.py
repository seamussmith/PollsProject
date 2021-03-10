from typing import Type
from django.db import models
from uuid import uuid4
from datetime import date, datetime
import json

class Poll(models.Model):
    question = models.TextField()
    pub_date = models.DateTimeField('date published')
    uuid = models.TextField(primary_key=True)

    # Method for creating a new poll
    # Method and not constructor because I did not want to override the default constructor
    @staticmethod
    def new(name, choices):
        new_uuid = str(uuid4()) # Generate UUID
        new_poll = Poll( # Return poll object (this is not saved to the database)
            question = name,
            uuid = new_uuid,
            pub_date = datetime.now()
        )
        new_poll.save()
        for choice in choices: # Create choice for each choice
            choice = Choice.new(choice, new_poll)
            choice.save()
        new_poll.save()
        return new_poll
    # Grab all the choices for the poll
    def get_choices(self):
        return self.choice_set.all()
    # Grab all choices as a dictionary with their uuid as the keys
    # ! Probably not a good idea to use...
    def get_choices_dict(self):
        result = {}
        for choice in self.get_choices():
            result[choice.uuid] = {
                "name": choice.name,
                "votes": choice.votes,
                "poll_uuid": choice.poll_uuid
            }
        return result
    # Convert poll to dictionary data
    def to_dict(self):
        return {
            "question": self.question,
            "uuid": self.uuid,
            "choices": [i.to_dict() for i in self.get_choices()],
            "pub_date": self.pub_date
        }
    # Reset each choice's votes
    def reset_poll(self):
        for choice in self.get_choices():
            choice.reset_vote()
    def __str__(self):
        return f"{self.question}:{'{'}{self.uuid}{'}'}"

class Choice(models.Model):
    name = models.TextField()
    votes = models.IntegerField()
    uuid = models.TextField(primary_key=True)
    poll_uuid = models.ForeignKey(Poll, on_delete=models.CASCADE)
    @staticmethod
    def new(name, poll_uuid):
        return Choice(
            name = name,
            poll_uuid = poll_uuid,
            uuid = str(uuid4()),
            votes = 0
        )
    # Convert choice data to a dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "votes": self.votes,
            "uuid": self.uuid,
            "poll_uuid": self.poll_uuid.uuid,
        }
    # Use these functions to modify the choice's votes in a safe way
    def inc_vote(self):
        self.votes += 1
    def dec_vote(self):
        self.votes -= 1
    def reset_vote(self):
        self.votes = 0
    def __str__(self):
        return f"{self.name}:{'{'}{self.uuid}{'}'}"


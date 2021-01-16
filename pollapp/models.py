from typing import Type
from django.db import models
from uuid import uuid4
from datetime import date
import json


# Create your models here.
# ? Maybe make an abstract class with these implmentations?
class Poll(models.Model):
    name = models.TextField()
    choices = models.TextField()
    uuid = models.TextField(primary_key=True)

    # I chose to make a static new method because I dont want to override the constructor
    # Returns a new Poll database object
    @staticmethod
    def new(data):
        return Poll(
            name = data["name"],
            choices = json.dumps(data["choices"]),
            uuid = data.get("uuid") or str(uuid4()),
        )

    # Returns data as a dict
    def to_dict(self):
        return {
            "name": self.name,
            "choices": json.loads(self.choices),
            "uuid": self.uuid
        }
    
    # Update Polls using a dict with new data
    def update(self, new_data):
        stored_data = self.to_dict()
        stored_data.update(new_data)
        self.name = stored_data["name"]
        self.choices = json.dumps(stored_data["choices"])
        self.uuid = stored_data["uuid"]
    
    # Increment the choice's votes by the value given.
    def inc_vote(self, index, value):
        data = self.to_dict()
        if type(index) is int:
            data["choices"][index]["votes"] += value
        else:
            raise TypeError("Index can only be of types (int)")
        self.update(data)

from django.db import models
from uuid import uuid4
from datetime import date
import json


# Create your models here.
class Poll(models.Model):
    name = models.TextField()
    choices = models.TextField()
    uuid = models.TextField(primary_key=True)

    @staticmethod
    def new(data):
        return Poll(
            name = data["name"],
            choices = json.dumps(data["choices"]),
            uuid = data.get("uuid") or str(uuid4()),
        )

    def to_dict(self):
        return {
            "name": self.name,
            "choices": json.loads(self.choices),
            "uuid": self.uuid
        }

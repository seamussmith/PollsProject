from django.db import models

# Create your models here.
class Poll(models.Model):
    name = models.TextField()
    choices = models.TextField()
    uuid = models.TextField()
    creation_date = models.DateTimeField()

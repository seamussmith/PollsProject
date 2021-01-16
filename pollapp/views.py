from django.http.response import Http404, HttpResponse
from django.shortcuts import render
#from django.db.backends.sqlite3 import *
from django.db.backends import sqlite3
from .models import *
import json

# Create your views here.
def index(request):
    if request.POST: # If the request is a POST requset, assuming this is a vote...
        body = request.POST
        # Get the uuid of the poll and the user's choice
        uuid = body.get("uuid")
        choice = int(body.get("choice"))
        # Query the database for the poll
        poll = next(i for i in Poll.objects.all() if i.uuid == uuid)
        # Increment the choice that the user chose by 1
        poll.inc_vote(choice, 1)
        # Save and return the new data for the poll as a JSON string
        poll.save()
        return HttpResponse(json.dumps(poll.to_dict()))
    # Else, assume it is a user trying to access the website
    polls = [i.to_dict() for i in Poll.objects.all()][:20] # Grab the first 20 polls you can get from the database
    return render(request, "pages/index.html", context={
        "polls": polls
    })

def contact(request):
    return render(request, "pages/contact.html", context={})

def placeholder(request):
    # TODO: Add a proper placeholder page (404?)
    return render(request, "PLACEHOLDER", context={})

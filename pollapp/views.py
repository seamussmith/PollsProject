from django.http.response import Http404, HttpResponse
from django.shortcuts import render
#from django.db.backends.sqlite3 import *
from django.db.backends import sqlite3
from .models import *
import json
from functools import reduce
from math import ceil, floor

# Create your views here.
def index(request):
    if not request.session.get("votes"):
        request.session["votes"] = {}
    if request.POST: # If the request is a POST requset, assuming this is a vote...
        body = request.POST
        # Get the uuid of the poll and the user's choice
        uuid = body.get("uuid")
        choice = int(body.get("choice"))
        # Query the database for the poll
        poll = Poll.objects.get(uuid=uuid)
        # Increment the choice that the user chose by 1
        if uuid in request.session["votes"]:
            poll.inc_vote(request.session["votes"][uuid], -1)
            request.session["votes"].pop(uuid)
        if not choice == request.session["votes"].get(uuid):
            poll.inc_vote(choice, 1)
            # Save and return the new data for the poll as a JSON string
            poll.save()
            #total = reduce(lambda x, y: x + y["votes"], data["choices"], 0)
            #for i in data["choices"]:
            #    i["percent"] = i["votes"]/total * 100
        data = poll.to_dict()
        request.session["votes"][uuid] = choice
        return HttpResponse(json.dumps(data))
    # Else, assume it is a user trying to access the website
    polls = [i.to_dict() for i in Poll.objects.all()][:20] # Grab the first 20 polls you can get from the database
    for i in polls:
        for j in i["choices"]:
            total = reduce(lambda x, y: x + y["votes"], i["choices"], 0) or 1
            j["precent"] = round(j["votes"]/total * 100)
    return render(request, "pages/index.html", context={
        "polls": polls
    })

def contact(request):
    return render(request, "pages/contact.html", context={})

def placeholder(request):
    # TODO: Add a proper placeholder page (404?)
    return render(request, "PLACEHOLDER", context={})

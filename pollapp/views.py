from django.http.response import Http404, HttpResponse
from django.shortcuts import render
#from django.db.backends.sqlite3 import *
from django.db.backends import sqlite3
from .models import *
import json

# Create your views here.
def index(request):
    if request.POST:
        body = request.POST
        uuid = body.get("uuid")
        choice = int(body.get("choice"))
        poll = next(i for i in Poll.objects.all() if i.uuid == uuid)
        poll.inc_vote(choice, 1)
        poll.save()
        return HttpResponse(json.dumps(poll.to_dict()))
    polls = [i.to_dict() for i in Poll.objects.all()][:20] # Grab the first 20 polls
    return render(request, "pages/index.html", context={
        "polls": polls
    })

def contact(request):
    return render(request, "pages/contact.html", context={})

def placeholder(request):
    # TODO: Add a proper placeholder page (404?)
    return render(request, "PLACEHOLDER", context={})

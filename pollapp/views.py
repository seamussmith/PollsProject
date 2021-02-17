from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
#from django.db.backends.sqlite3 import *
from django.db.backends import sqlite3
from .models import *
import json
from functools import reduce
from math import ceil, floor
from django import forms

# Create your views here.
def index(request):
    # TODO: Refactor POST handle into different view
    # Else, assume it is a user trying to access the website
    polls = list(reversed([i.to_dict() for i in Poll.objects.all()])) # Grab the first 20 polls you can get from the database
    for i in polls:
        total = reduce(lambda x, y: x + y["votes"], i["choices"], 0) or 1
        for j in i["choices"]:
            j["precent"] = round(j["votes"]/total * 100)
    return render(request, "pages/index.html", context={
        "polls": polls,
        "votes": request.session.get("votes")
    })

def contact(request):
    return render(request, "pages/contact.html", context={})

def validate_poll_form(data):
    errors = []
    if data.get("name") == "":
        errors.append("Form must have a name")
    if len(data.getlist("choice[]")) == 0:
        errors.append("Poll must have at least one choice")
    for i, choice in enumerate(data.getlist("choices")):
        if len(choice) > 20:
            errors.append(f"Choice {i+1} must be less than 40 characters long")
    if len(data.get("name")) > 100:
        errors.append(f"Question must be less than 100 characters long")
    return errors

def submit_poll(request):
    if request.POST:
        body = request.POST
        errors = validate_poll_form(body)
        if len(errors) != 0:
            return render(request, "pages/create-poll.html", context={
                "errors": errors
            })
        choices = body.getlist("choice[]")
        name = body.get("name")
        new_poll = Poll.new(name, choices)
        new_poll.save()
    return render(request, "pages/create-poll.html", context={
        "errors": []
    })

def grab_polls(request):
    next_poll = int(request.GET.get("next"))
    polls = list(reversed([i.to_dict() for i in Poll.objects.all()]))[next_poll:next_poll+20]
    return render(request, "pages/grab-polls.html", {
        "polls": polls
    })

def placeholder(request):
    # TODO: Add a proper placeholder page (404?)
    return HttpResponse("PLACEHOLDER")

@require_http_methods(["POST"])
def poll_vote(request):
    # TODO: I know you will not forgive me future me, but there is ALOT of spaghetti you have to clean up... 
    if request.session.get("votes") is None: # if there is no storage for votes...
        request.session["votes"] = {}
    body = request.POST
    # Get the uuid of the poll and the user's choice
    uuid = body.get("uuid")
    choice_id = body.get("choice")
    prev_choice = request.session["votes"].get(uuid) # Grab the user's previous vote for this poll
    same_vote = request.session["votes"].get(uuid) == choice_id
    # Query the database for the poll
    # Increment the choice that the user chose by 1
    if uuid in request.session["votes"]: # If the user already voted on this poll
        prev = Choice.objects.get(uuid=prev_choice)
        prev.votes -= 1 # Decrement the user's previous choice
        prev.save()
        request.session["votes"].pop(uuid) # Remove the record of the vote
    if not same_vote: # If this was a different choice
        choice = Choice.objects.get(uuid=choice_id)
        choice.votes += 1 # Increment the vote of the choice by 1
        choice.save()
        request.session["votes"][uuid] = choice_id # Save the vote to the user's session
    # Save and return the new data for the poll as a JSON string
    data = Poll.objects.get(uuid=uuid).to_dict()
    print(request.session["votes"])
    return HttpResponse(json.dumps(data))

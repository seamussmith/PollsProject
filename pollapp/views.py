from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import *
import json
from functools import reduce
from math import ceil, floor
from django import forms

# Create your views here.
def index(request):
    if request.session.get("votes") is None: # if there is no storage for votes...
        request.session["votes"] = {}
    polls = list(reversed([i.to_dict() for i in Poll.objects.all()])) # Grab the first 20 polls you can get from the database
    return render(request, "pages/index.html", context={
        "polls": polls,
        "votes": request.session.get("votes")
    })

def contact(request):
    return render(request, "pages/contact.html", context={})

def validate_poll_form(data):
    errors = []
    if data.get("name").isspace():
        errors.append("Form must have a name")
    if len(data.getlist("choice[]")) == 0:
        errors.append("Poll must have at least one choice")
    for i, choice in enumerate(data.getlist("choice[]")):
        print(choice)
        if len(choice) > 20:
            errors.append(f"Choice {i+1} must be less than 40 characters long")
        if choice.isspace():
            errors.append(f"Choice {i+1} must not be whitespace")
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
        choices = [i for i in choices if not i.isspace() and i != ""]
        print(choices)
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
    if request.session.get("votes") is None: # if there is no storage for votes...
        request.session["votes"] = {}
    
    body = request.POST
    # Get the uuid of the poll and the user's choice
    poll_uuid = body.get("uuid")
    choice_id = body.get("choice")
    prev_choice_id = request.session["votes"].get(poll_uuid) # Grab the user's previous vote for this poll
    is_same_vote = request.session["votes"].get(poll_uuid) == choice_id

    # Increment the choice that the user chose by 1
    if poll_uuid in request.session["votes"]: # If the user already voted on this poll
        prev = Choice.objects.get(uuid=prev_choice_id) # Grab previous choice from database
        prev.dec_vote() # Decrement the user's previous choice
        prev.save()
        request.session["votes"].pop(poll_uuid) # Remove the record of the vote from session
    
    if not is_same_vote: # If this was a different choice
        choice = Choice.objects.get(uuid=choice_id) # Grab choice from database
        choice.inc_vote() # Increment the vote of the choice by 1
        choice.save()
        request.session["votes"][poll_uuid] = choice_id # Save the vote to the user's session
    
    data = Poll.objects.get(uuid=poll_uuid).to_dict() # Grab poll data from database
    return JsonResponse(data) # Return poll data as JSON string

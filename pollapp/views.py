from django.http.response import Http404, HttpResponse
from django.shortcuts import render
#from django.db.backends.sqlite3 import *
from django.db.backends import sqlite3

# Create your views here.
def index(request):
    if request.POST:
        return HttpResponse(f"{request.POST}")
    polls = [{
            "name": f"Awesome Poll #{i}",
            "choices": [
                {"text": "Choice 1", "votes": 0},
                {"text": "Choice 2", "votes": 0},
                {"text": "Choice 3", "votes": 0},
            ],
            "uuid": i
        } for i in range(0, 21)]
    return render(request, "pages/index.html", context={
        "polls": polls
    })

def contact(request):
    return render(request, "pages/contact.html", context={})

def placeholder(request):
    # TODO: Add a proper placeholder page (404?)
    return render(request, "PLACEHOLDER", context={})

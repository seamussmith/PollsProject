from django.http.response import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.POST:
        return HttpResponse(f"{request.POST}")
    polls = []
    for i in range(0, 21):
        polls.append({
            "name": f"Awesome Poll #{i}",
            "choices": [
                {"text": "Choice 1", "votes": 0},
                {"text": "Choice 2", "votes": 0},
                {"text": "Choice 3", "votes": 0},
            ],
            "uuid": i
        })
    return render(request, "pages/index.html", context={
        "polls": polls
    })

def contact(request):
    return render(request, "pages/contact.html", context={})

def placeholder(request):
    # TODO: Add a proper placeholder page (404?)
    return render(request, "PLACEHOLDER", context={})

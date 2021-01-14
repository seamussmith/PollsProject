from django.http.response import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.POST:
        return HttpResponse(f"{request.POST}")
    return render(request, "pages/index.html", context={})

def contact(request):
    return render(request, "pages/contact.html", context={})

def placeholder(request):
    # TODO: Add a proper placeholder page (404?)
    return render(request, "PLACEHOLDER", context={})

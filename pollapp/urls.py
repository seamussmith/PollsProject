from django.urls import path
from . import views

app_name = "pollapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.placeholder, name="about"),
    path("contact/", views.contact, name="contact"),
    path("submit-poll/", views.submit_poll, name="submit-poll"),
    path("settings/", views.placeholder, name="settings"),
    path("grab-polls/", views.grab_polls, name="grab-polls"),
    path("poll-vote/", views.poll_vote, name="poll-vote")
]

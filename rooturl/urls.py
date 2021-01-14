from django.urls import path
from . import views

app_name = "rooturl"
urlpatterns = [
    path("", views.index, name="index")
]

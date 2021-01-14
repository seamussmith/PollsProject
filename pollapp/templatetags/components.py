from django.template.defaulttags import register
from django.template.loader import render_to_string

@register.inclusion_tag("components/poll.html")
def CreatePoll(poll, delay=0):
    return ({
        "delay": delay,
        "poll": poll
    })

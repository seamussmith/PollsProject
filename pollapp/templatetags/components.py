from django.template.defaulttags import register

@register.inclusion_tag("components/poll.html")
def CreatePoll(poll, delay=0):
    return {
        "delay": delay,
        "poll": poll
    }

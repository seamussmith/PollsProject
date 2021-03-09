from django.template.defaulttags import register
from functools import reduce

@register.inclusion_tag("components/poll.html")
def CreatePoll(poll, vote, delay=0):
    return {
        "delay": delay,
        "poll": poll,
        "vote": vote,
        "total": (reduce(lambda a, b: a + b["votes"], poll["choices"], 0) or 1),
        "pub_date": poll["pub_date"].date()
    }

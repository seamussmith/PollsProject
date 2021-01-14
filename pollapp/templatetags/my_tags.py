from django.template.defaulttags import register
from django.template.loader import render_to_string

@register.filter()
def seq(mini, maxi):
    return range(mini, maxi)

@register.filter()
def mul(a, b):
    return str(float(a) * float(b))
 
@register.inclusion_tag()
def CreatePoll(poll, i=0):
    return render_to_string("components/poll.html", context={
        "i": i,
        "poll": poll
    })

from django.template.defaulttags import register

@register.filter()
def seq(mini, maxi):
    return range(mini, maxi)

@register.filter()
def mul(a, b):
    return str(float(a) * float(b))
 

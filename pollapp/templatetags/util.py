from django.template.defaulttags import register

# range
@register.filter()
def seq(mini, maxi):
    return range(mini, maxi)

# Maths and stuff
@register.filter()
def add(a, b):
    return str(float(a) + float(b))

@register.filter()
def sub(a, b):
    return str(float(a) - float(b))

@register.filter()
def mul(a, b):
    return str(float(a) * float(b))
 
@register.filter()
def div(a, b):
    return str(float(a) / float(b))

@register.filter()
def mod(a, b):
    return str(float(a) % float(b))

@register.filter(name='lookup')
def lookup(value, arg):
    return value.get(arg)

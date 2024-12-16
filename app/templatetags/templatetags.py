from datetime import datetime, timezone
from django import template

register = template.Library() 

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

# @register.filter
# def hello_world():
#     now = datetime.now().date()
#     return now.year


# @register.filter
# def hello_world():
    # greet = 'hello' 
    # return hello 
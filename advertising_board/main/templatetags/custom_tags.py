from random import randint

from django import template


register = template.Library()
register.simple_tag(lambda: randint(0, 100), name='notifications')

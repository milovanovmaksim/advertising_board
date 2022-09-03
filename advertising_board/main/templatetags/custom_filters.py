from django import template


register = template.Library()


def reverse_string(value):
    return ''.join(value[::-1])


register.filter('reverse_string', reverse_string)

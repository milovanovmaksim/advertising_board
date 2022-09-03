from urllib.parse import urlencode

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def url_encode(context, **kwargs):
    url_params = dict(context['request'].GET)
    for key, value in kwargs.items():
        if value:
            url_params[key] = value
    return urlencode(url_params, doseq=True)

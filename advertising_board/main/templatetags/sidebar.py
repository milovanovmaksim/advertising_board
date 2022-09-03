from django import template

from ..models import Tag


register = template.Library()


@register.inclusion_tag('main/tags.html')
def show_tags():
    tags = Tag.objects.all()
    return {'tags': tags}

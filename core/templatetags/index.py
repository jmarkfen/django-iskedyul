from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.simple_tag
def classes(key):
    cons = {
        'card': 'card border-primary-subtle rounded-0',
    }
    return cons[key]
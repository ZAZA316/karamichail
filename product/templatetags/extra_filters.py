from django import template

register = template.Library()


@register.filter
def get_by_index(l, i):
    return l[i]


@register.filter
def limit_description(description):
    return description[:30] + '...'

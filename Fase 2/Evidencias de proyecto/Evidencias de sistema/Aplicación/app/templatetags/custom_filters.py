from itertools import groupby
from operator import attrgetter
from django import template

register = template.Library()

@register.filter
def groupby(value, arg):
    # Ordena `value` por el atributo `arg` antes de aplicar `groupby`
    sorted_value = sorted(value, key=attrgetter(arg))
    return {k: list(v) for k, v in groupby(sorted_value, key=attrgetter(arg))}

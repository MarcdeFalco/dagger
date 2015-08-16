import textile

from django.conf import settings
from django.utils.encoding import smart_str, force_text
from django.utils.safestring import mark_safe
from django import template


register = template.Library()

def roman(n):
    r = [ '', 'I', 'II', 'III', 'IV',
            'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI' ]
    return r[n]

def alpha(n):
    return chr(ord('a')+n)

def paragraph_number(par):
    anc = list(par.get_ancestors(include_self=True))[1:]
    if len(anc) > 3:
        return ''
    if len(anc) == 0:
        return ''
    s = roman(anc[0].order)
    if len(anc) > 1:
        s += '-'+str(anc[1].order)
    if len(anc) > 2:
        s += '-'+alpha(anc[2].order)
    return s

paragraph_number.is_safe = True

register.filter(paragraph_number)

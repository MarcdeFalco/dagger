import textile

from django.conf import settings
from django.utils.encoding import smart_str, force_text
from django.utils.safestring import mark_safe
from django import template

from knowledge.format import convert_references

register = template.Library()

def atom_format(value):
    l = []
    lines = value.replace('\r','').split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('jxg:'):
            arguments = line[len('jxg:'):]
            args = arguments.split()
            boxid = args[0]

            boxwidth = int(args[1])
            boxheight = int(args[2])

            if len(args) == 3 + 4:
                rect = tuple(map(float, args[3:]))
            else:
                rect = (-boxwidth//100, boxheight//100, boxwidth//100, -boxheight//100)

            l.append("notextile.. <div id='jxgbox%s' class='jxgbox' style='width:%dpx; height:%dpx;'></div><script type='text/javascript'>" % (boxid, boxwidth, boxheight))
            l.append("var brd%s = JXG.JSXGraph.initBoard('jxgbox%s', " % (boxid, boxid) \
                    + "{boundingbox: [%d,%d,%d,%d], showCopyright: false});" \
                        % rect)

            i += 1
            while i < len(lines) and lines[i] != '':
                l.append( lines[i] )
                i += 1

            l.append('</script>')
            l.append('')
        else:
            l.append(lines[i])
            i += 1
    value = '\r\n'.join(l)

    html = textile.textile(convert_references(value))
    return mark_safe(html)

atom_format.is_safe = True

register.filter(atom_format)

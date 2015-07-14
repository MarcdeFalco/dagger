import re

# A reference to an atom
# "le théorème plop":applique:245 by id
# "link desc":verb:ref
reference_re_s = r'''"(?P<desc>[^"]*)":(?P<verb>\w+):(?P<ref>[_\w]+)'''
reference_re = re.compile(reference_re_s)

def extract_references(value):
    l = []
    for match in re.finditer(reference_re, value):
        # desc = match.group('desc')
        verb = match.group('verb')
        ref = match.group('ref')
        l.append( (verb, ref) )
    return l

def convert_references(value):
    from knowledge.models import Atom
    i0 = 0
    converted = ''
    for match in re.finditer(reference_re, value):
        i, j = match.span()
        converted += value[i0:i]
        desc = match.group('desc')
        #verb = match.group('verb')
        ref = match.group('ref')

        try:
            atom = Atom.objects.by_ref(ref)
            url = atom.get_absolute_url()

            if desc != 'silent':
                converted += '"%s":%s' % (desc, url)
        except:
            converted += '"(orphan)%s":/admin/knowledge/atom/add/?slug=%s&source=main' % (desc, ref)

        i0 = j
    converted += value[i0:]
    return converted


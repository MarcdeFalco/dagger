from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from knowledge.models import Atom, AtomType, AtomRelationship
# from random import choice

# Create your models here.

class Paragraph(MPTTModel):
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True,
                related_name='children', db_index=True)
    order = models.PositiveSmallIntegerField(default=1)
    content = models.ManyToManyField(Atom, through='ParagraphContainsAtoms')
    handout = models.ForeignKey('Handout')

    def ordered_content(self):
        return self.content.all().order_by('paragraphcontainsatoms__order')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['order']

class ParagraphContainsAtoms(models.Model):
    paragraph = models.ForeignKey(Paragraph)
    lead_in = models.TextField(blank=True)
    atom = models.ForeignKey(Atom)
    lead_out = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order',]

class Handout(models.Model):
    lead = models.ForeignKey(Paragraph, blank=True, null=True, related_name='handout_as_lead')
    cluster = models.BooleanField(default=False)
    code = models.TextField(help_text='''
Handout code format :<br/>
<br/>
Lead paragraph<br/>
* Main paragraph<br/>
** Sub paragraph<br/>
<br/>
In each paragraph, you can reference atoms:<br/>
Direct reference<br/>
- atom_by_ref<br/>
Reference by relationships<br/>
-> verb atom_by_ref [(all,random,first)]<br/>
Create a new atom and reference it<br/>
-{ typ_slug [slug [name]]<br/>
Atom text goes here<br/>
}<br/>
<br/>
After each atom references you can add text: <br/>
text placed just before the atom to introduce it and can be multiline<br/>
-- (optional separation and signal that )<br/>
the following lines are to be placed after the atom<br/>
''')

    def atoms(self):
        atoms = []

        for paragraph in self.lead.get_descendants(include_self=True):
            for atom in paragraph.content.filter(typ__important=True):
                if atom not in atoms:
                    atoms.append(atom)

        return atoms

    def __str__(self):
        return self.lead.name

    def save(self, *save_args, **kwargs):
        super(Handout, self).save(*save_args, **kwargs)
        old_lead = self.lead

        lines = self.code.replace('\r','').split('\n') 
        branch = []
        suborder = 1

        lead = Paragraph.objects.create(name=lines[0],
                slug=slugify(lines[0]), handout=self)
        lead.save()
        branch = [ (lead, 1) ]

        processed_lines = [lines[0]]

        def get_tag(i):
            if i >= len(lines):
                return None
            line = lines[i]
            if line == '' or line.strip() == '':
                return None
            return line.strip().split()[0]

        i = 1
        while i < len(lines):
            line = lines[i]
            tag = get_tag(i)
            i += 1
            if line == '':
                processed_lines.append(line)
                continue
            if tag.startswith('-'):
                if tag == '-':
                    processed_lines.append(line)
                    ref = line.split()[1]
                    atom = Atom.objects.by_ref(ref)
                elif tag == '->':
                    processed_lines.append(line)
                    args = line.split()
                    verb = args[1]
                    ref = args[2]

                    # TODO
                    # mult = 'first'
                    # if len(args) > 3:
                    #    mult = args[3]

                    atom = Atom.objects.by_ref(ref)
                    ar = AtomRelationship.objects.get(to_atom=atom,
                            typ__slug=verb)
                    atom = ar.from_atom
                elif tag == '-{':
                    args = line.split()
                    typ_slug = args[1]
                    slug = None
                    name = None
                    if len(args) > 2:
                        slug = args[2]
                        if len(args) > 3:
                            name = ' '.join(args[3:])
                    typ = AtomType.objects.get(slug=typ_slug)
                    atom = Atom.objects.create(typ=typ)
                    if slug:
                        atom.slug = slug
                    atom_text = []
                    while i < len(lines):
                        line = lines[i]
                        i += 1
                        if line != '' and line[0] == '}':
                            break
                        atom_text.append( line )
                    atom.text = '\n'.join(atom_text)
                    atom.slug = slug
                    if name:
                        atom.name = name
                    atom.save()
                    if slug:
                        processed_lines.append('- ' + slug)
                    else:
                        processed_lines.append('- ' + str(atom.id))

                paragraph, _ = branch[-1]
                lead_in = []
                lead_out = []
                leading_out = False
                while i < len(lines):
                    t = get_tag(i)
                    if not t:
                        processed_lines.append(lines[i])
                        i += 1
                        continue
                    if t == '--':
                        leading_out = True
                        processed_lines.append(lines[i])
                        i += 1
                        continue
                    if t[0] in ['-', '*']:
                        break
                    processed_lines.append(lines[i])
                    if leading_out:
                        lead_out.append( lines[i].strip() )
                    else:
                        lead_in.append( lines[i].strip() )
                    i += 1
                lead_in = '\r\n'.join(lead_in)
                lead_out = '\r\n'.join(lead_out)
                pca = ParagraphContainsAtoms.objects.create(paragraph=paragraph,
                        atom=atom, order=suborder,
                        lead_in=lead_in, lead_out=lead_out)
                pca.save()
                suborder += 1
            elif set(tag) == {'*'}:
                processed_lines.append(line)
                suborder = 1
                level = 1 + len(tag)
                name = line.strip()[len(tag):].strip()
                slug = slugify(name)
                if level <= len(branch):
                    while len(branch) > level:
                        branch.pop()
                    _, old_order = branch.pop()
                    order = old_order + 1
                else:
                    order = 1
                parent, _ = branch[-1]
                par = Paragraph.objects.create(name=name, slug=slug,
                        parent=parent, order=order, handout=self)
                par.save()
                branch.append( (par, order) )
        self.lead = lead
        self.code = '\n'.join(processed_lines)
        super(Handout, self).save(*save_args, **kwargs)
        if old_lead:
            old_lead.delete()


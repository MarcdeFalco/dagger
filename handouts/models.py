from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from knowledge.models import Atom, AtomRelationship
from random import choice

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
    code = models.TextField()

    def __str__(self):
        return self.lead.name

    def save(self, *save_args, **kwargs):
        super(Handout, self).save(*save_args, **kwargs)
        old_lead = self.lead

        # Handout code format :
        # ---------------------
        # Lead paragraph
        # * Main paragraph
        # ** Sub paragraph
        # - atom_by_ref
        # text placed just before the atom to introduce it
        # and can be multiline
        # -- (optional separation and sign that )
        # the following lines are to be placed after the atom
        # -> verb atom_by_ref [(all,random,first)]

        lines = self.code.replace('\r','').split('\n') 
        branch = []
        suborder = 1

        lead = Paragraph.objects.create(name=lines[0],
                slug=slugify(lines[0]), handout=self)
        lead.save()
        branch = [ (lead, 1) ]

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
                continue
            if tag == '-':
                ref = line.split()[1]
                atom = Atom.objects.by_ref(ref)
                paragraph, _ = branch[-1]
                lead_in = []
                lead_out = []
                leading_out = False
                while i < len(lines):
                    t = get_tag(i)
                    if not t:
                        i += 1
                        continue
                    if t == '--':
                        leading_out = True
                        i += 1
                        continue
                    if t[0] in ['-', '*']:
                        break
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
            elif tag == '->':
                args = line.split()
                verb = args[1]
                ref = args[2]

                mult = 'first'
                if len(args) > 3:
                    mult = args[3]

                atom = Atom.objects.by_ref(ref)
                ar = AtomRelationship.objects.get(to_atom=atom,
                        typ__slug=verb)
                paragraph, _ = branch[-1]
                pca = ParagraphContainsAtoms.objects.create(paragraph=paragraph,
                        atom=ar.from_atom, order=suborder)
                pca.save()
                suborder += 1
            elif set(tag) == {'*'}:
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
        super(Handout, self).save(*save_args, **kwargs)
        if old_lead:
            old_lead.delete()


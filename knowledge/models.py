from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from knowledge.db import SlugOrNullField


class ContentRevision(models.Model):
    atom = models.ForeignKey('Atom')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [ '-date', ]

class AtomType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30,unique=True)
    bootstrap_label = models.CharField(max_length=30, default='default')

    def __str__(self):
        return self.name

class AtomRelationshipType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30,unique=True)

    def __str__(self):
        return u'%s' % self.name

class AtomManager(models.Manager):
    def by_ref(self, ref):
        try:
            id = int(ref)
            return self.get(id=id)
        except ValueError:
            return self.get(slug=ref)

class Atom(models.Model):
    name = models.CharField(max_length=200, blank=True)
    slug = SlugOrNullField(max_length=60,unique=True,blank=True,null=True)
    typ = models.ForeignKey(AtomType)
    text = models.TextField()
    relationships = models.ManyToManyField('self',
            through='AtomRelationship',
            symmetrical=False,
            related_name='related_to')
    date = models.DateTimeField(auto_now_add=True)
    objects = AtomManager()

    def __str__(self):
        ref = ''
        if self.name != '':
            ref = str(self.name)
        elif self.slug != None:
            ref = str(self.slug)
        else:
            ref = str(self.id)
        return u'%s %s' % (str(self.typ), ref)

    def get_absolute_url(self):
        return reverse('atom_detail', kwargs={'pk' : self.id})

    def save(self, *args, **kwargs):
        old_slug = None
        if self.pk is not None:
            old_self = Atom.objects.get(pk=self.pk)
            old_slug = old_self.slug

        super(Atom, self).save(*args, **kwargs)
        # reify any orphan relationship
        for orphan_rel in AtomOrphanRelationship.objects.filter(ref=self.slug):
            reify_rel = AtomRelationship.objects.create(from_atom=orphan_rel.atom,
                    to_atom=self, typ=orphan_rel.typ)
            reify_rel.save()
            orphan_rel.delete()

        from knowledge.format import extract_references, replace_references
        # fix references when slug is changed
        if self.slug != old_slug:
            if old_slug is None or old_slug == '':
                old_ref = str(self.pk)
            else:
                old_ref = old_slug

            if self.slug is None or self.slug == '':
                new_ref = str(self.pk)
            else:
                new_ref = self.slug

            rels = AtomRelationship.objects.filter(to_atom=self)

            for rel in rels: 
                atom = rel.from_atom
                atom.text = replace_references(atom.text, old_ref, new_ref)
                atom.save()

        # extract references and test for relationships
        uptodate_rel = []
        for verb, ref in extract_references(self.text):
            try:
                reltype = AtomRelationshipType.objects.get(slug=verb)
            except ObjectDoesNotExist:
                continue
            try:
                atom = Atom.objects.by_ref(ref)
                try:
                    existing_rel = AtomRelationship.objects.get(from_atom=self,
                            to_atom=atom, typ=reltype)
                    uptodate_rel.append(existing_rel)
                except ObjectDoesNotExist:
                    arel = AtomRelationship.objects.create(from_atom=self,
                            to_atom=atom, typ=reltype)
                    arel.save()
                    uptodate_rel.append(arel)
            except ObjectDoesNotExist:
                arel = AtomOrphanRelationship.objects.create(atom=self,
                        ref=ref, typ=reltype)
                arel.save()
        extra_rel = AtomRelationship.objects.filter(from_atom=self) \
                .exclude(id__in=[ rel.id for rel in uptodate_rel ])
        for extra in extra_rel:
            extra.delete()

class AtomOrphanRelationship(models.Model):
    ref = models.SlugField(max_length=60)
    atom = models.ForeignKey(Atom)
    typ = models.ForeignKey(AtomRelationshipType)

class AtomRelationship(models.Model):
    from_atom = models.ForeignKey(Atom, related_name='from_atoms')
    to_atom = models.ForeignKey(Atom, related_name='to_atoms')
    typ = models.ForeignKey(AtomRelationshipType)


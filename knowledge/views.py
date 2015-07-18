from django.shortcuts import render

from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, FormView, RedirectView, DeleteView, View

from django import forms

from knowledge.models import *
import re

class AtomDetail(DetailView):
    model = Atom
    context_object_name = 'atom' 

class AtomDAG(ListView):
    model = Atom
    context_object_name = 'atoms' 
    template_name = 'knowledge/atom_dag.html'

class AtomBulkForm(forms.Form):
    source = forms.CharField(widget=forms.Textarea)

    def clean_source(self):
        source = self.cleaned_data['source']
        # Atom bulk format
        # $Atom <atom type slug> 
        # $Ref [internal ref]
        # $Slug <slug>
        # $Name <name>
        # ... text ...

        lines = source.replace('\r','').split('\n')

        i = 0

        current_atom = None
        atoms = []

        for line in lines:
            if line == '':
                continue
            if line[0] == '$':
                tokens = line[1:].split()
                command = tokens[0]
                arg = line[1+len(command):].strip()

                if command.lower() == 'atom':
                    if current_atom is not None:
                        if 'ref' not in current_atom:
                            current_atom['ref'] = str(len(atoms)+1)
                        atoms.append(current_atom)
                    current_atom = { 'type' : arg, 'text' : '' }

                if command.lower() == 'ref':
                    current_atom['ref'] = arg

                if command.lower() == 'slug':
                    current_atom['slug'] = arg

                if command.lower() == 'name':
                    current_atom['name'] = arg
            elif current_atom is not None:
                current_atom['text'] += line + '\r\n'

        if current_atom is not None:
            if 'ref' not in current_atom:
                current_atom['ref'] = str(len(atoms)+1)
            atoms.append(current_atom)

        slug_re = re.compile(r'^[\w_]+$')

        from knowledge.format import extract_references
        edges_incoming = {}
        edges_outgoing = {}

        atom_by_ref = {}
        for atom in atoms:
            atom['refs'] = extract_references(atom['text'])
            aref = atom['ref']
            atom_by_ref[aref] = atom
            edges_outgoing[aref] = []
            if aref not in edges_incoming:
                edges_incoming[aref] = []
            for _, ref in atom['refs']:
                if ref[0] == '$':
                    if ref[1:] not in edges_incoming:
                        edges_incoming[ref[1:]] = []
                    edges_incoming[ref[1:]].append(aref)
                    edges_outgoing[aref].append(ref[1:])
                    
        s = []
        for atom in atoms:
            if edges_outgoing[atom['ref']] == []:
                s.append(atom)
            atom['outgoing'] = []


        ordered = []

        while len(s) > 0:
            a = s[0]
            ordered.append(a)
            s = s[1:]
            for oaref in edges_incoming[a['ref']]:
                edges_outgoing[oaref].remove(a['ref'])
                atom_by_ref[oaref]['outgoing'].append( a )
                if edges_outgoing[oaref] == []:
                    s.append(atom_by_ref[oaref])

        for atom in atoms:
            if edges_outgoing[atom['ref']] != []:
                raise forms.ValidationError("Cycle impliquant $%s" % atom['ref'])

        for atom in atoms:
            if 'slug' in atom and slug_re.match(atom['slug']) is None:
                raise forms.ValidationError("Slug invalide %s" % atom['slug'])

            typ = atom['type']
            if AtomType.objects.filter(slug=typ).count() == 0:
                raise forms.ValidationError("Type inconnu %s" % typ)

        self.ordered = ordered

        return source

    def create_atoms(self):
        from knowledge.format import replace_references

        for atom in self.ordered:
            typ = AtomType.objects.get(slug=atom['type'])

            text = atom['text']
            for oatom in atom['outgoing']:
                text = replace_references(text,
                        '$'+oatom['ref'], str(oatom['id']))

            ra = Atom.objects.create(typ=typ,text=text)
            if 'name' in atom:
                ra.name = atom['name']
            if 'slug' in atom:
                ra.slug = atom['slug']
            ra.save()
            atom['id'] = ra.id

class AtomBulkView(FormView):
    template_name = 'knowledge/atom_bulk.html'
    form_class = AtomBulkForm
    success_url = '/k/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_atoms()
        return super(AtomBulkView, self).form_valid(form)


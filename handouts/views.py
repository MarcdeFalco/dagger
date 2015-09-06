from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, FormView, RedirectView, DeleteView, View
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, Http404

from handouts.models import *
from knowledge.models import *

import json

class HandoutDetail(DetailView):
    model = Handout
    context_object_name = 'handout' 

class TexHandoutDetail(DetailView):
    model = Handout
    context_object_name = 'handout' 
    template_name = 'handouts/handout_detail.tex'
    content_type = 'application/tex'


class HandoutList(ListView):
    model = Handout
    context_object_name = 'handouts' 

class HandoutDAGjson(View):
    model = Handout
    context_object_name = 'handout' 

    def get_atoms(self, handout):
        atoms = []

        for paragraph in handout.lead.get_descendants(include_self=True):
            for atom in paragraph.content.filter(typ__important=True):
                if atom not in atoms:
                    atoms.append(atom)

        return atoms

    def get(self, request, *args, **kwargs):
        handout = get_object_or_404(Handout, pk=kwargs['pk'])
        atoms = self.get_atoms(handout)

        graph = { 'nodes' : [], 'links' : [] }
        for atom in atoms:
            a = { 'id' : atom.id, 'group' : atom.typ.bootstrap_label }
            if atom.slug:
                a['name'] = atom.slug
            else:
                a['name'] = str(atom.id)
            a['full_name'] = str(atom)
            a['url'] = atom.get_absolute_url()
            graph['nodes'].append(a)

        for atom in atoms:
            a = { 'name' : atom.name, 'group' : atom.typ.id }
            for rel in atom.from_atoms.all():
                if rel.to_atom in atoms:
                    link = { 'source' : atom.id,
                            'target' : rel.to_atom.id,
                            'value' : rel.typ.slug }
                    graph['links'].append(link)
            for to_atom, rel_typ in atom.fuse_from_atoms():
                if to_atom in atoms:
                    link = { 'source' : atom.id,
                            'target' : to_atom.id,
                            'value' : rel_typ.slug }
                    graph['links'].append(link)

        return HttpResponse(json.dumps(graph),
                content_type='application/json')


class HandoutDAG(DetailView):
    model = Handout
    context_object_name = 'handout' 
    template_name = 'knowledge/atom_dag.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HandoutDAG, self).get_context_data(*args, **kwargs)
        handout = self.get_object()
        
        context['json'] = '/h/dag/' + str(handout.id) + '/json/'

        return context

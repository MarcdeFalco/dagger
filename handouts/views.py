from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, FormView, RedirectView, DeleteView, View

from handouts.models import *

class HandoutDetail(DetailView):
    model = Handout
    context_object_name = 'handout' 

class HandoutList(ListView):
    model = Handout
    context_object_name = 'handouts' 

class HandoutDAG(DetailView):
    model = Handout
    context_object_name = 'handout' 
    template_name = 'knowledge/atom_dag.html'

    def get_context_data(self, *args, **kwargs):
        from knowledge.models import AtomRelationshipType

        context = super(HandoutDAG, self).get_context_data(*args, **kwargs)
        context['types'] = AtomRelationshipType.objects.all()

        handout = self.get_object()

        atoms = []

        for paragraph in handout.lead.get_descendants(include_self=True):
            for atom in paragraph.content.all():
                if atom not in atoms:
                    atoms.append(atom)

        context['atoms'] = atoms

        return context

from django.shortcuts import render

from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, FormView, RedirectView, DeleteView, View

from knowledge.models import *

class AtomDetail(DetailView):
    model = Atom
    context_object_name = 'atom' 

class AtomDAG(ListView):
    model = Atom
    context_object_name = 'atoms' 
    template_name = 'knowledge/atom_dag.html'

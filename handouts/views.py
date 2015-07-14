from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, FormView, RedirectView, DeleteView, View

from handouts.models import *

class HandoutDetail(DetailView):
    model = Handout
    context_object_name = 'handout' 

class HandoutList(ListView):
    model = Handout
    context_object_name = 'handouts' 

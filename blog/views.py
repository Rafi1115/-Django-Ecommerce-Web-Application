from django.shortcuts import render

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, TemplateView
)

class Lol(TemplateView):
    template_name = 'som.html'
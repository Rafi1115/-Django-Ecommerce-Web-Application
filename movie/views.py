from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
import django
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.cache import cache
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, TemplateView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
)
from django.core.exceptions import (
    PermissionDenied
)
from .models import Movie, Person, TvMovie, TvName, Celebrite
from blog.models import Category, NewsMovie

class IndexView(ListView):
    model = Movie
    # template_name = 'movie/index.html'
    template_name = 'prac/person.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        self.slider = Movie.objects.all()[:6]
        # self.tv = TvMovie.objects.filter(movie__startswith='d')
        self.tvmovie = TvMovie.objects.all().filter(id='4')
        self.celebrite = Celebrite.objects.all()[:4]
        self.person = Person.persons.all_with_movies()
        self.category = Category.objects.all()
        self.blog = NewsMovie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = {
            'slider':self.slider,
            'tvmovie':self.tvmovie,
            'celebrite': self.celebrite,
            'person': self.person,
            'category':self.category,
            'blog':self.blog
            # 'tv':self.tv,
        }
        return context




class PersonDetail(DetailView):
    model = Person
    template_name = 'prac/index.html'
    context_object_name = 'queryset'

# def get_queryset(self):
# self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
# return Book.objects.filter(publisher=self.publisher)

    # def get_queryset(self):
    #     self.person = Person.objects.all_with_movies()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = Person.objects.all_with_movies()
    
        
        context = {
          'person':person,
   
        }
    
        return context


# class PersonList(ListView):

#     queryset = Person.shit.all_with_prefetch_movies()

# class PersonList(ListView):

#     model = TvMovie
#     template_name = 'prac/person.html'
#     context_object_name = 'queryset'

    # def get_context_data(self, *args, **kwargs):

    #     shit = TvMovie.objects.all()
    #     context = {

    #         'shit':shit,

        
    #     }
    #     return context

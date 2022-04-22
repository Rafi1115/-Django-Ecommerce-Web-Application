
from django.urls import path

from .import views



urlpatterns = [

    path('',views.Lol.as_view(), name='IndexView'),



]


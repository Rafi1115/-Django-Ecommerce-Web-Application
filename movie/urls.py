
from django.urls import path

from .import views

app_name = 'movie'

urlpatterns = [

    path('',views.IndexView.as_view(), name='IndexView'),
    path('person/<int:pk>', views.PersonDetail.as_view(), name='PersonDetail'),


]






# urlpatterns = [
#     path('', views.PersonList.as_view(), name='list')
# ]
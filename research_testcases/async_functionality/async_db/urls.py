from django.urls import path

from . import views


urlpatterns = [
    path('add_person', views.add_person, name='add_person'),
    path('search', views.search, name='search'),
]
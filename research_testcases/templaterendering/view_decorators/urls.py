from django.urls import path

from . import views

urlpatterns = [
    path('index_post', views.index_post, name='index_post'),
    path('index_get', views.index_get, name='index_get'),
    path('both', views.both, name='both'),
]
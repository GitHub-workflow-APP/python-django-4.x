from django.urls import path

from . import views

urlpatterns = [
    path('simple_form_subclassing/', views.simple_form_subclassing, name='simple_form_subclassing'),
   ]
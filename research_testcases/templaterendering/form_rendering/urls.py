from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form_rendering_template/', views.form_rendering_template, name='form_rendering_template'),
    path('form_rendering_template_FP/', views.form_rendering_template_FP, name='form_rendering_template_FP'),

]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('formset_httpresponse/', views.formset_httpresponse, name='formset_httpresponse'),
    path('formset_template_rendering/', views.formset_template_rendering, name='formset_template_rendering'),
    #path('formset_xss', views.formset_xss, name='formset_xss'),
    #path('formset_template', views.formset_template, name='formset_template'),
    #path('formset_template_filter', views.formset_template_filter, name='formset_template_filter'),
]

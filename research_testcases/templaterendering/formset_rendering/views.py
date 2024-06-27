from django.http import HttpResponse
from django import forms
from django.forms import formset_factory
import datetime
from django.utils.safestring import mark_safe
from django.shortcuts import render

class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

# Attack Payload: curl 'http://localhost:8000/formset_rendering/formset_template_rendering/'  -X POST -d 'name=<script>alert(1)</script>'
def formset_httpresponse(request):
    ArticleFormSet = formset_factory(ArticleForm)

    # It's an XSS at the return HttpResponse line only when tainted data is marked safe for HTML escaping via mark_safe method.
    formset = ArticleFormSet(data=[{'title':mark_safe(request.POST.get('name')),'pub_data':datetime.date.today(),}]) # CWEID 80

    ret_data = ''

    for form in formset:
        ret_data += form.as_table().replace("\n","")

    return HttpResponse("Hello from formset_httpresponse " + ret_data) # CWEID 80

# Attack Payload: curl 'http://localhost:8000/formset_rendering/formset_template_rendering/'  -X POST -d 'name=<script>alert(1)</script>'
def formset_template_rendering(request):
    ArticleFormSet = formset_factory(ArticleForm)
    # Unescaped data makes it to template
    formset = ArticleFormSet(initial=[{'title':mark_safe(request.POST.get('name')),'pub_data':datetime.date.today(),}]) # CWEID 80
    return render(request, 'manage_articles.html', {'formset': formset, 'tainted_name': request.POST.get('name')})


def index(request):
    return HttpResponse("Hello, world. You're at the formset_app index.")
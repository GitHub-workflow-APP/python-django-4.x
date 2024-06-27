# Attack Payload: curl 'http://localhost:8000/form_field_rendering/home/' -X POST -d 'name=<Mansi>&email=<msheth@veracode.com>&message=<HelloWorld>&no=<script>alert(1)</script>'
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from django.utils.safestring import SafeString

def home(request):

    form = ContactForm(request.POST)

    for x in form.data.keys():
	    print(x + " : " + SafeString(form.data.get(x))) # CWEID 80

    safeseq_lst = []
    safeseq_lst.append(request.POST.get('name'))
    safeseq_lst.append(request.POST.get('email'))
    safeseq_lst.append(request.POST.get('message'))

    return render(request, 'home.html', {'form': form,'name':request.POST.get('name'),'safeseq_lst':safeseq_lst})

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

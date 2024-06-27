from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse
from django.utils.safestring import mark_safe

# Attack Payload : curl 'http://localhost:8000/form_rendering/form_rendering_template/' -X POST -d 'name=<script>alert(1)</script>&email=<script>alert(1)</script>.gmail.com&message=<script>alert(1)</script>'
def form_rendering_template(request):
    initial = {'name':mark_safe(request.POST.get('name')), # CWEID 80
              'email':mark_safe(request.POST.get('email')), # CWEID 80
             'message':mark_safe(request.POST.get('message')),} # CWEID 80

    form = ContactForm(data=initial)

    return render(request, 'form_rendering_template.html', {'form': form,})

# Attack Payload: curl 'http://localhost:8000/form_rendering/form_rendering_template_FP/' -X POST -d 'name=<script>alert(1)</script>&email=<script>alert(1)</script>.gmail.com&message=<script>alert(1)</script>'
def form_rendering_template_FP(request):
    form = ContactForm(request.POST) # Data is not marked safe before being initialized in the ContactForm
    return render(request,'form_rendering_template_FP.html', {'form': form,})

def index(request):
    return HttpResponse("Hello, world. You're at the form_rendering index.")
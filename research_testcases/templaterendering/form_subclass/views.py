from django.shortcuts import render
from .forms import PersonForm, InstrumentForm, BeatleForm
from django.utils.safestring import SafeString

def simple_form_subclassing(request):
    initial = {'name': SafeString(request.POST.get('name')), # CWEID 80
               'instrument': SafeString(request.POST.get('instrument')), # CWEID 80
               'haircut_type': SafeString(request.POST.get('hair_cut')), # CWEID 80

    }
    form = BeatleForm(initial=initial)
    return render(request, 'simple_form_subclassing.html', {'form':form})



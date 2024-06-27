from django import forms

class PersonForm(forms.Form):
    name = forms.CharField()

class InstrumentForm(forms.Form):
    instrument = forms.CharField()

class BeatleForm(InstrumentForm, PersonForm):
    haircut_type = forms.CharField()


from django import forms

class ContactForm(forms.Form):

    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(max_length=2000)
    # I could pass taint in a Decimal and Float Fields as well. But there could be some configuration which enabled that.
    # Just as being overly conservative lets not report on that
    no = forms.DecimalField(localize=False)


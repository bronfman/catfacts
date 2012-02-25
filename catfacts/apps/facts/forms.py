from django import forms

class FactForm(forms.Form):
    fact = forms.CharField(max_length=120)


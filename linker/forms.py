from django import forms


class LinkCreationForm(forms.Form):
    link = forms.CharField(widget=forms.Textarea)

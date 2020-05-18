from django import forms


# Form for creation new link
class LinkCreationForm(forms.Form):
    # Just one field :)
    link = forms.CharField(widget=forms.Textarea)  # Full link in model

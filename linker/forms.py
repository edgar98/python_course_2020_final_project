from django import forms


# Form for creation new link
class LinkCreationForm(forms.Form):
    # Just one field :)
    link = forms.CharField(widget=forms.TextInput({
        'placeholder': 'Write your link here',
        'label': ''}))  # Full link in model

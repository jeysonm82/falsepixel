from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(max_length=150)
    message = forms.CharField(max_length=400, widget=forms.widgets.Textarea())
    captcha= forms.CharField(max_length=4)
    email = forms.EmailField()


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.CharField(max_length=150)
    message = forms.CharField(max_length=400, widget=forms.widgets.Textarea())


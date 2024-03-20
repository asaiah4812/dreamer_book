from django.forms import ModelForm
from users.models import Profile
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ( 'user', )
        
# This form is used to create
        labels = {
            'realname':"Name"
        }
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows':3})
        }
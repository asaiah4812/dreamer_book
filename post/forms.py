from django import forms
from django.forms import ModelForm
from .models import *

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {
            'body': 'caption',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add a caption ...', 'class': 'font1 text-4xl'}),
            'url' : forms.TextInput(attrs={'placeholder': 'Add url ...'}),
            'tags' : forms.CheckboxSelectMultiple(),
        }
        
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {
            'body': 'caption',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add a caption ...', 'class': 'font1 text-4xl'}),
            'url' : forms.TextInput(attrs={'placeholder': 'Add url ...'}),
            'tags' : forms.CheckboxSelectMultiple(),
        }
        
class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add comment ...'})
        }
        labels = {
            'body': ''
        }
        
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add reply ...', 'class': "!text-sm"})
        }
        labels = {
            'body': ''
        }

        

        
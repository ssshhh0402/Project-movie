from django import forms
from .models import Movie, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('movie','user')
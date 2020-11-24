from django import forms
from .models import MovieComment


class MovieCommentForm(forms.ModelForm):

    class Meta:
        model = MovieComment
        fields = ['rank', 'content']
        # exclude = ['movie', 'user']
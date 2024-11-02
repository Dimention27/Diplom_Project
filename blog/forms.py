from django import forms

from .models import New


class PostForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ('title', 'text', 'image')


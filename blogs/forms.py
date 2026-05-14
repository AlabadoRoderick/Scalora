from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'excerpt', 'image', 'tags', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control scalora-input'}),
            'tags': forms.TextInput(attrs={'class': 'form-control scalora-input', 'placeholder': 'tag1, tag2, tag3'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

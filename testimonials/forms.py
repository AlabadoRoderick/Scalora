from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'position', 'message', 'rating', 'avatar', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'position': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'message': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-select scalora-input'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control scalora-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

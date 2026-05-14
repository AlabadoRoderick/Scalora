from django import forms
from .models import Ebook, EbookOrder

class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['title', 'description', 'author', 'cover_image', 'price', 'pages', 'category', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 4}),
            'author': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control scalora-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control scalora-input', 'step': '0.01'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control scalora-input'}),
            'category': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = EbookOrder
        fields = ['quantity', 'notes']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control scalora-input', 'min': 1, 'max': 10}),
            'notes': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 3, 'placeholder': 'Any special instructions or payment details...'}),
        }

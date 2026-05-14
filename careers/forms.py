from django import forms
from .models import JobPosting

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'department', 'job_type', 'location', 'description', 'requirements', 'salary_range', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'department': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'job_type': forms.Select(attrs={'class': 'form-select scalora-input'}),
            'location': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 5}),
            'requirements': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 5}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control scalora-input', 'placeholder': 'e.g. $50,000 - $70,000'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

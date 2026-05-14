from django import forms
from .models import Service, AdminSchedule


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control scalora-input', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control scalora-input', 'step': '0.01'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control scalora-input'}),
            'icon': forms.TextInput(attrs={'class': 'form-control scalora-input', 'placeholder': 'e.g. bi-briefcase'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AdminScheduleForm(forms.ModelForm):
    class Meta:
        model = AdminSchedule
        fields = ['date', 'start_time', 'end_time', 'is_available', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control scalora-input', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control scalora-input', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control scalora-input', 'type': 'time'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.TextInput(attrs={'class': 'form-control scalora-input'}),
        }

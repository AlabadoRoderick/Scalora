from django import forms
from .models import Appointment
from services.models import Service


class AppointmentForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select scalora-input'}),
        empty_label='Select a Service'
    )
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control scalora-input', 'type': 'date', 'id': 'booking-date'
    }))
    time_slot = forms.TimeField(widget=forms.Select(attrs={
        'class': 'form-select scalora-input', 'id': 'time-slot-select'
    }))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control scalora-input', 'rows': 3,
        'placeholder': 'Any additional notes or special requests...'
    }))

    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time_slot', 'notes']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')
        if date and time_slot:
            existing = Appointment.objects.filter(
                date=date, time_slot=time_slot, status__in=['pending', 'confirmed']
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError('This time slot is already booked. Please choose another.')
        return cleaned_data

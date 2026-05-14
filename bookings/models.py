from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    meet_link = models.URLField(blank=True, help_text='Google Meet or video call link sent to client on confirmation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.username} - {self.service.name} on {self.date} at {self.time_slot}"

    def time_slot_end(self):
        """Return end time = start + 30 minutes."""
        from datetime import datetime, timedelta
        end = (datetime.combine(self.date, self.time_slot) + timedelta(minutes=30)).time()
        return end

    class Meta:
        ordering = ['-date', '-time_slot']
        unique_together = ['date', 'time_slot']
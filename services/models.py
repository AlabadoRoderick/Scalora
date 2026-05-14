from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    icon = models.CharField(max_length=100, blank=True, default='bi-briefcase')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def duration_display(self):
        if self.duration < 60:
            return f"{self.duration} min"
        hours = self.duration // 60
        minutes = self.duration % 60
        if minutes:
            return f"{hours}h {minutes}m"
        return f"{hours}h"

    class Meta:
        ordering = ['name']


class AdminSchedule(models.Model):
    """Admin's available time slots for booking"""
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.date} {self.start_time} - {self.end_time}"

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['date', 'start_time']

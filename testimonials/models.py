from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i,i) for i in range(1,6)])
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"

    class Meta:
        ordering = ['-created_at']

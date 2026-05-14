from django.db import models
from django.contrib.auth.models import User


class Ebook(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    author = models.CharField(max_length=200, default='Scalora Team')
    cover_image = models.ImageField(upload_to='ebook_covers/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class EbookOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Payment Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ebook_orders')
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} – {self.ebook.title} by {self.client.username}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.ebook.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-ordered_at']

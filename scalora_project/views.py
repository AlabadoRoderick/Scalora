"""Main project views for Scalora landing pages."""

from django.shortcuts import render
from testimonials.models import Testimonial
from services.models import Service
from blogs.models import Blog


def home(request):
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    services = Service.objects.filter(is_active=True)[:6]
    latest_blogs = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]
    context = {
        'testimonials': testimonials,
        'services': services,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')

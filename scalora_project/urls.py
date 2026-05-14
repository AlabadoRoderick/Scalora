"""Scalora URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as project_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', project_views.home, name='home'),
    path('about/', project_views.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
    path('bookings/', include('bookings.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('blogs/', include('blogs.urls')),
    path('careers/', include('careers.urls')),
    path('ebooks/', include('ebooks.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

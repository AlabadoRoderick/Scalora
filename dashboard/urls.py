from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    # Admin
    path('admin/', views.admin_home, name='admin_home'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/services/', views.admin_services, name='admin_services'),
    path('admin/testimonials/', views.admin_testimonials, name='admin_testimonials'),
    path('admin/blogs/', views.admin_blogs, name='admin_blogs'),
    path('admin/careers/', views.admin_careers, name='admin_careers'),
    path('admin/ebooks/', views.admin_ebooks, name='admin_ebooks'),
    # Client
    path('client/', views.client_home, name='client_home'),
    path('client/bookings/', views.client_bookings, name='client_bookings'),
    path('client/orders/', views.client_orders, name='client_orders'),
]

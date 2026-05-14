from django.urls import path
from . import views
app_name = 'testimonials'
urlpatterns = [
    path('', views.testimonials_list, name='list'),
    path('add/', views.add_testimonial, name='add'),
    path('<int:pk>/edit/', views.edit_testimonial, name='edit'),
    path('<int:pk>/delete/', views.delete_testimonial, name='delete'),
]
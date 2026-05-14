from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel'),
    path('<int:pk>/status/', views.update_appointment_status, name='update_status'),
]

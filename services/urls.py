from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='list'),
    path('<int:pk>/', views.service_detail, name='detail'),
    path('add/', views.add_service, name='add'),
    path('<int:pk>/edit/', views.edit_service, name='edit'),
    path('<int:pk>/delete/', views.delete_service, name='delete'),
    path('api/slots/', views.get_available_slots, name='available_slots'),
    path('api/available-dates/', views.get_available_dates, name='available_dates'),
    path('schedule/<int:pk>/toggle/', views.toggle_schedule, name='toggle_schedule'),
    path('schedule/<int:pk>/delete/', views.delete_schedule, name='delete_schedule'),
]
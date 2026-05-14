from django.urls import path
from . import views
app_name = 'careers'
urlpatterns = [
    path('', views.careers_list, name='list'),
    path('<int:pk>/', views.job_detail, name='detail'),
    path('add/', views.add_job, name='add'),
    path('<int:pk>/delete/', views.delete_job, name='delete'),
]

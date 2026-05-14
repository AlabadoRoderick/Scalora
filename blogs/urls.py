from django.urls import path
from . import views
app_name = 'blogs'
urlpatterns = [
    path('', views.blog_list, name='list'),
    path('add/', views.add_blog, name='add'),
    path('<slug:slug>/', views.blog_detail, name='detail'),
    path('<slug:slug>/edit/', views.edit_blog, name='edit'),
    path('<slug:slug>/delete/', views.delete_blog, name='delete'),
]

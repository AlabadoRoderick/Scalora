from django.urls import path
from . import views
app_name = 'ebooks'
urlpatterns = [
    path('', views.ebook_store, name='store'),
    path('<int:pk>/', views.ebook_detail, name='detail'),
    path('<int:pk>/order/', views.order_ebook, name='order'),
    path('add/', views.add_ebook, name='add'),
    path('<int:pk>/edit/', views.edit_ebook, name='edit'),
    path('order/<int:pk>/status/', views.update_order_status, name='update_order_status'),
    path('order/<int:pk>/receipt/', views.generate_receipt, name='receipt'),
]

from django.urls import path
from .views import (
        Dashboard, 
        MenuDetails,
        AddMenu,
        MakeOrder,
        Order,
        OrderNow,
    )

app_name = 'restaurant'
urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard-restaurant'),
    path('order/', Order.as_view(), name='order-restaurant'),
    path('menu-item/<int:pk>/', MenuDetails.as_view(), name='menu-order'),
    path('add-menu/', AddMenu.as_view(), name='add-menu-item'),
    path('make-order/', MakeOrder.as_view(), name='make-order'),
    path('orders/',OrderNow.as_view(),name='restaurant-orders'),
]

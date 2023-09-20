from django.urls import path
from .views import (
    OrderNow
)

app_name = 'customer'

urlpatterns = [
    path('orders/', OrderNow.as_view(), name='customer-orders'),
]
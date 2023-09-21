from django.urls import path
from .views import (
    OrderNow,
    EditProfile,
)

app_name = 'customer'

urlpatterns = [
    path('orders/', OrderNow.as_view(), name='customer-orders'),
    path('edit-profile/',EditProfile.as_view(),name='edit-customer-profile')
]
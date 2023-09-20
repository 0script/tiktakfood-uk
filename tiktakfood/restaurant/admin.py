from django.contrib import admin

from .models import (
    Restaurant,
    CategoryMenu,
    RestaurantMenu,
    ItemQuantity,
    WhishList,
    OrderRestaurant
)

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(CategoryMenu)
admin.site.register(RestaurantMenu)
admin.site.register(WhishList)
admin.site.register(ItemQuantity)
admin.site.register(OrderRestaurant)
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=254)
    restaurant_phone=models.CharField(max_length=254)
    restaurant_email=models.EmailField(max_length=254,blank=True,null=True)
    restaurant_address=models.CharField(max_length=254)
    restaurant_profile=models. ImageField(upload_to='profile_picture',blank=True,null=True)

    def get_absolute_url(self):
        return reverse('restaurant:restaurant-profile',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class RestaurantMenu(models.Model):
    name = models.CharField(max_length=100)
    ingredient = models.TextField()
    image = models.ImageField(upload_to='restaurant_images/')
    price = models.IntegerField()
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )
    category = models.ManyToManyField('CategoryMenu', related_name='item')
    cuisson_time=models.IntegerField(default=30)
    for_people=models.IntegerField(default=4)
    creation_date = models.DateField( auto_now_add=True)

    class Meta:
        ordering = ('creation_date' ,)

    def get_absolute_url(self):
        return reverse('restaurant:menu-order', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class CategoryMenu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WhishList(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    creation_date=models.DateField( auto_now_add=True)


    class Meta():
        ordering=('-creation_date',)

    def __str__(self):
        return self.customer.username+str(self.creation_date)

class OrderRestaurant(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    creation_date=models.DateField( auto_now_add=True)
    delivered_date=models.DateField(blank=True,null=True)
    is_ready=models.BooleanField(default=False)
    delivery=models.BooleanField(default=True)
    delivered=models.BooleanField(default=False)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE,blank=True,null=True)

class ItemQuantity(models.Model):
    menu_item=models.ForeignKey(RestaurantMenu,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    whishlist=models.ForeignKey(WhishList,on_delete=models.PROTECT,blank=True,null=True)
    order=models.ForeignKey(OrderRestaurant,on_delete=models.CASCADE,blank=True,null=True)


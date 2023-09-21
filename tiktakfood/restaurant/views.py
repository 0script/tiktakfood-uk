from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel
from django.contrib.auth.models import User

from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q

import json

from .forms import RegistrationForm,AddMenuForm
from .models import (
    Restaurant,
    RestaurantMenu,
    CategoryMenu,
    ItemQuantity,
    WhishList,
    OrderRestaurant,    
)


# Create your views here.


class RestaurantRegistration(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return render(request,'restaurant/registration.html')
        else:
            return redirect('/forbiden/')
    def post(self,request,*args,**kwargs):
        if request.method=='POST':
            print('form')

            print(request.POST)
            form=RegistrationForm(request.POST)
            if form.is_valid():

                queryset=Restaurant.objects.filter(user__username__iexact=request.user.username)
                
                if queryset.exists():
                    print('already in user')
                    context={
                        'formError':'You register with another restaurant'
                    }
                    return render(request,'restaurant/registration.html',context=context)
                else: 
                    print('is valid')

                    name = form.cleaned_data["name"]
                    restaurant_phone = form.cleaned_data["restaurant_phone"]
                    restaurant_address = form.cleaned_data["restaurant_address"]
                    restaurant_email = form.cleaned_data["restaurant_email"]
                    restaurant_profile = request.FILES.get('profile')
                    
                    print('rrr')
                    print(restaurant_profile)
                    
                    print(name,restaurant_address,restaurant_phone,restaurant_profile)
                    user=User.objects.get(id=request.user.id)
                    print(user)
                    if restaurant_profile :
                        if restaurant_email:
                            restaurant=Restaurant.objects.create(
                                user=user,
                                name=name,
                                restaurant_address=restaurant_address,
                                restaurant_phone=restaurant_phone,
                                restaurant_email=restaurant_email,
                                restaurant_profile=restaurant_profile
                            )
                        else:
                            restaurant=Restaurant.objects.create(
                                user=user,
                                name=name,
                                restaurant_address=restaurant_address,
                                restaurant_phone=restaurant_phone,
                                restaurant_email=restaurant_email,
                                restaurant_profile=restaurant_profile
                            )
                    if restaurant_email:
                        print('email')
                        try:
                            restaurant=Restaurant.objects.create(
                                user=user,
                                name=name,
                                restaurant_address=restaurant_address,
                                restaurant_phone=restaurant_phone,
                                restaurant_email=restaurant_email,
                            )
                        except Exception as e:
                            print('exception')
                            print(e)
                            pass
                    
                    restaurant.save()
                    request.session['restaurant']=restaurant.id
                    return redirect('/restaurant/dashboard')
            else:
                print(form.errors['__all__'].as_text())

                context={
                    'formError':form.errors['__all__'].as_text()
                }
                return render(request,'restaurant/registration.html',context=context)

class Dashboard(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated :
            if 'restaurant' not in request.session :
                query=Restaurant.objects.filter(user=request.user)
                if not query.exists():
                    return redirect('/forbiden/')
                else:
                    restaurant=query.first()
                    request.session['restaurant']=restaurant.id
            else:
                restaurant=Restaurant.objects.get(id=request.session['restaurant'])
            context={
                'restaurant':restaurant
            }
            return render(request,'restaurant/dashboard.html',context)
        else:
            return redirect('/forbiden/')

class AddMenu(View):
        def get(self,request,*args,**kwargs):
            if request.user.is_authenticated:
                
                if not request.session['restaurant']:
                    query=Restaurant.objects.filter(user=request.user)
                    if not query.exists():
                        return redirect('/forbiden/')
                    else:
                        request.session['restaurant']=query.id
                restaurant=Restaurant.objects.get(id=request.session['restaurant'])
                context={
                    'restaurant':restaurant
                }
                return render(request,'restaurant/add-menu.html',context)
            else:
                return redirect('/forbiden/')

        def post(self,request,*args,**kwargs):
            if request.user.is_authenticated and request.session['restaurant']:
                restaurant=Restaurant.objects.get(id=request.session['restaurant'])
                print(request.POST)
                
                form=AddMenuForm(request.POST)
                
                print('form added')
                if form.is_valid():
                    print('cleaned',form.cleaned_data['name'])
                    name=request.POST['name']
                    ingredient=request.POST['ingredient']
                    price=request.POST['price']
                    cuisson_time=request.POST['cuisson_time']
                    for_people=request.POST['for_people']

                    category=request.POST['category']
                    restaurant=Restaurant.objects.get(id=request.session['restaurant'])
                    category=CategoryMenu.objects.filter(name__contains=category)
                    
                    if category.exists():
                        menu_item=RestaurantMenu(
                            name=name,
                            ingredient=ingredient,
                            image=request.FILES['picture'],
                            price=price,
                            restaurant=restaurant,
                            cuisson_time=cuisson_time,
                            for_people=for_people
                        )

                        print(request.FILES['picture'])
                        menu_item.save()
                        menu_item.category.set(category)
                        print('saved')
                        return redirect('/restaurant/dashboard')
                    
                    else:
                        
                        category=CategoryMenu.objects.create(name=request.POST['category'])
                        category.save()
                        menu_item=RestaurantMenu(
                            name=name,
                            ingredient=ingredient,
                            image=request.FILES['picture'],
                            price=price,
                            restaurant=restaurant,
                            cuisson_time=cuisson_time,
                            for_people=for_people,
                        )

                        print(request.FILES['picture'])
                        menu_item.save()
                        menu_item.category.set(category)
                        print('saved')
                        return redirect('/restaurant/dashboard')
                else:
                    print('not valid')
                    return render(request,'restaurant/add-menu.html',{'formError':'This field is requiered'})
            else:
                return redirect('/forbiden/')

class MenuRestaurant(View):
    def get(self,request,*args,**kwargs):
        menu_items=reversed(RestaurantMenu.objects.all())
        context={
            'menu_items':menu_items
        }
        return render(request,'restaurant/menu.html',context)



class MenuRestaurantSearch(View):
    def get(self,request,*args,**kwargs):
        query=self.request.GET.get('q')
        
        menu_items=RestaurantMenu.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(ingredient__icontains=query)
        )

        context={
            'menu_items':menu_items
        }
        
        return render(request,'restaurant/menu.html',context)

class MenuDetails(View):
    def get(self,request,pk,*args,**kwargs):
        print(pk)
        request.session['page']='MenuDetails'
        menu=RestaurantMenu.objects.filter(id=pk).get()
        context={
            'menu':menu
        }
        return render(request,'restaurant/menu-detail.html',context)

class MakeOrder(View):
    def post(self,request,*args,**kwargs):
        if request.method=='POST' and request.user.is_authenticated:
            jsonData=json.loads(request.body)
            print(jsonData)

            print(jsonData['order_now'])
            
            quantity=jsonData['quantity']
            menu_id=jsonData['menu_id']
            order_now=jsonData['order_now']
            menu_item=RestaurantMenu.objects.filter(id=menu_id).get()


            if order_now is False:

                print('saving objc')

                whishlist=WhishList.objects.filter(customer__username=request.user.username)
                print(whishlist)

                if whishlist.exists():
                    print('ok')
                    whishlist=whishlist.first()
                    
                    print('id')
                    print(whishlist.customer.username)
                    print(whishlist.id)

                    query_menu_item=Q(menu_item__id=menu_id)
                    query_whishlist=Q(whishlist__pk=whishlist.id)
                    
                    item_quantity=ItemQuantity.objects.filter(query_menu_item & query_whishlist)

                    if item_quantity.exists():
                        item_quantity=item_quantity.get()
                        item_quantity.quantity+=quantity
                        item_quantity.save()
                    else:
                        item_quantity=ItemQuantity(
                            menu_item=menu_item,
                            quantity=quantity,
                            whishlist=whishlist
                        )
                        item_quantity.save()
                else:
                    whishlist=WhishList(customer=request.user)
                    item_quantity=ItemQuantity(menu_item=menu_item,quantity=quantity,whishlist=whishlist)
                    whishlist.save()
                    item_quantity.save()
                
                print('saved')
                return JsonResponse({'result':'success'})
            else:
                print('creating order')

                # get restaurant 
                restaurant=Restaurant.objects.get(id=menu_item.restaurant.id)
                print(restaurant)

                # check if restaurant has order with this  
                # customer and the delivery status
                query_customer=Q(customer=request.user.id)
                query_delivered=Q(delivered=False)

                order=OrderRestaurant.objects.filter(query_customer & query_delivered)
                if order.exists():
                    print('exist')
                    query_menu_item=Q(menu_item=menu_item)
                    query_order=Q(order=order.first().id)
                    item_quantity=ItemQuantity.objects.filter(query_menu_item & query_order)
                    if item_quantity.exists():
                        item_quantity=item_quantity.first()
                        item_quantity.quantity+=quantity
                        item_quantity.whishlist=None
                        item_quantity.save()

                    else:
                        print('item quantity do not exist ')
                        print('the order is ',order)
                        item_quantity=ItemQuantity.objects.create(
                            menu_item=menu_item,
                            quantity=quantity,
                            order=order.get()
                        )
                        item_quantity.save()
                        
                    return JsonResponse({'result':'success'})
                else:
                    order=OrderRestaurant(
                        customer=request.user,
                        restaurant=restaurant,
                    )
                    order.save()
                    item_quantity=ItemQuantity(
                        menu_item=menu_item,
                        quantity=quantity,
                        order=order
                    )
                    item_quantity.save()
                    print('order added')
                    return JsonResponse({'result':'success'})

            return JsonResponse({'result':'errror'})
        else:
            return JsonResponse({'result':'error'})

class OrderNow(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['page']='OrderNow'
            context={
                'orders':'',
                'item_quantity':'',
            }
            restaurant=Restaurant.objects.filter(user=request.user.id).get()
            orders=OrderRestaurant.objects.all()
            print('the orders ',orders)
            item_quantity=ItemQuantity.objects.filter(menu_item__restaurant=restaurant.id)

            if item_quantity.exists():
                print('item exist')
                order_list=[]

                print('looping')
                print(orders)
                for order in orders:
                    
                    print('the order')
                    print(order.id)
                    for item in item_quantity:
                        if item.order != None :
                            if order.id==item.order.id:
                                print('the item is ')
                                order_list.append(order.id)
                
                print('priting')
                print(order_list)
                order=OrderRestaurant.objects.filter(pk__in=order_list)
                print(order)

                context={
                    'item_quantity':item_quantity,
                    'orders':orders,
                }

            print('context is ',orders)
            return render(request,'restaurant/orders.html',context)
        else:
            return redirect('/login/')
    def post(self,request,*args,**kwargs):
        if request.method=='POST' and request.user.is_authenticated:
            jsonData=json.loads(request.body)
            print(jsonData)

            action=jsonData['action']
            order_id=jsonData['order']
            order=OrderRestaurant.objects.get(id=order_id)
            
            print('action and order')
            print(action,' and ',order_id)

            if action.get('shipped'):
                print('action shipped')
                if order.is_ready:
                    order.is_ready=False
                else:
                    order.is_ready=True
            if action.get('ordered'):
                if order.ordered:
                    order.ordered=False
                else:
                    order.ordered=True
            if action.get('on-the-way'):
                if order.is_ready:
                    order.is_ready=False
                else:
                    order.is_ready=True
            if action.get('on-the-way'):
                if order.delivered:
                    order.delivered=False
                else:
                    order.delivered=True
               
            order.save()
            print('saved')
            return JsonResponse({'result':'success'})
        else:
            return JsonResponse({'result':'error'})

class Order(View):
    def get(self, request, *args, **kwargs):

        # if request.user.is_authenticated and request.session['restaurant']:            
        if request.user.is_authenticated :            
            # get the current date
            today = datetime.today()
            # orders = OrderModel.objects.filter(
            #     created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

            # loop through the orders and add the price value, check if order is not shipped
            unshipped_orders = []
            total_revenue = 0
            # for order in orders:
            #     total_revenue += order.price

            #     if not order.is_shipped:
            #         unshipped_orders.append(order)

            # pass total number of orders and total revenue into template
            context = {
                'orders': unshipped_orders,
                'total_revenue': 1000,
                'total_orders': 7
            }

            return render(request, 'restaurant/order.html', context)
        else:
            return redirect('/forbiden/')

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        request.session['page']='OrderNow'
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
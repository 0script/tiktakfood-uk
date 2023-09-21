import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import (
    MenuItem, 
    Category, 
    OrderModel,
    Customer
)
from .forms import RegistrationForm
from restaurant.models import (
    WhishList,
    ItemQuantity,
    RestaurantMenu,
    OrderRestaurant,
)

class Index(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/menu/')
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Login(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/login.html')

    def post(self,request,*argc,**kwargs):
        print('post login')
        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            print(username,password)
            user=authenticate(request,username=request.POST['username'],password=request.POST['password'])

            if user is not None:
                print('auth ok')
                login(request,user)
                menu_items = MenuItem.objects.all()
                request.session['username']=user.username                
                return redirect('/menu/')
            else:
                print('not ok')
                errors_msg='Username or password incorect'
                context={
                    'errors_msg':errors_msg,
                }

                print(context)

                return render(request,'customer/login.html',context)


class Registration(View):
    
    def get(self,request,*args,**kwargs):
        return render(request,'customer/registration.html')
    
    def post(self,request,*args,**kwargs):
    
        if request.method=='POST':
            form=RegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                phone = form.cleaned_data["phone"]
                address = form.cleaned_data["address"]
                birthday=form.cleaned_data["birthday"]
                gender=form.cleaned_data['gender']
                password=form.cleaned_data['password']


                # print(request.POST.get('profile'))
                # print(request.FILES.get('photo'))
                # if request.POST['profile']=='':
                #     profile=''
                # else:
                #     profile=request.FILES['profile']
                # print(request.FILES['picture'])

                new_user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )

                new_user.save()

                if request.FILES['profile']:
                    print('profile')
                    print(request.FILES.get('profile'))
                    profile=request.FILES.get('profile')

                    print(profile)
                    customer=Customer(
                        user=new_user,
                        phone=phone,
                        address=address,
                        profile=profile
                    )
                else:
                    customer=Customer(
                        user=new_user,
                        phone=phone,
                        address=address,
                    )
                    print('empty')
                
                customer.save()
                print('customer ok')
                print(customer.user.username)
                user=authenticate(username=username,password=password)
                login(request,user)
                menu_items = MenuItem.objects.all()

                request.session['username']=request.POST['username']
                return redirect('/menu/')
            else:
                errors={}
                for e in form.errors:
                    errors[str(e)]=form.errors[e].as_text()
                
                context={
                    'formError':errors
                }
                return render(request,'customer/registration.html',context=context)
        
class EditProfile(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/edit-profile.html')
    def post(self,request,*args,**kwargs):
        
        if request.method=='POST':
            request.session['page']='EditProfile'
            print(request)
            # context={
                
            # }
            return render(request,'customer/edit-profile.html')

class DashboardCustomer(View):
    def get(self,request,*args,**kwargs):
        print(request.user)
        print(request.user.id)
        print(request.user)

        if request.user.is_authenticated:
            print(request.user.customer)
            return render(request,'customer/dashboard.html')
        else:
            return redirect('/forbiden/')

class Forbiden(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/forbiden.html')

class OrderNow(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            
            request.session['page']='OrderNow'
            context={
                'whishlist':'',
                'item_quantity':'',
                'orders':'',
                'item_quantity_order':''
            }
            # check for whishlist 
            whishlist=WhishList.objects.filter(customer=request.user.id)
            if whishlist.exists():
                
                print('exists')
                item_quantity=ItemQuantity.objects.filter(whishlist=whishlist.get().id)
                context['whishlist']=whishlist.get
                context['item_quantity']=item_quantity
                print(context)
            
            order=OrderRestaurant.objects.filter(customer=request.user.id)
            if order.exists():
                print('order exist')
                item_quantity_order=ItemQuantity.objects.all()
                context['orders']=order
                context['item_quantity_order']=item_quantity_order
            else:
                print('no order')
                order=''

            print('the list of wish')
            print(context['whishlist'])
            return render(request,'customer/order.html',context)
        else:
            return redirect('/login/')
    def post(self,request,*args,**kwargs):
        if request.method=='POST' and request.user.is_authenticated:
            jsonData=json.loads(request.body)
            print(jsonData)
            item_quantity_id=jsonData['item_quantity']
            print(item_quantity_id)

            item_quantity=ItemQuantity.objects.get(id=item_quantity_id)
            customer=Q(customer=request.user.id)
            delivered=Q(delivered=False)
            order=OrderRestaurant.objects.filter(customer & delivered)
            if order.exists():
                order=order.get()
                item_quantity.whishlist=None
                item_quantity.order=order
                item_quantity.save()
            else:
                print('Restaurant id order creation ')
                print(item_quantity.menu_item.restaurant.id)
                restaurant_id=item_quantity.menu_item.restaurant.id
                order=OrderRestaurant(customer=request.user,restaurant=restaurant_id)
                order.save()
                item_quantity.order=order
                item_quantity.save()
            
            whishlist=WhishList.objects.filter(customer=request.user.id)
            if whishlist.exists():
                query_whishlist=Q(whishlist__pk=whishlist.get().id)
                item_quantity=ItemQuantity.objects.filter(query_whishlist)
                if not item_quantity.exists():
                    print('deleting')
                    whishlist.get().delete()
            
            return JsonResponse({'result':'success'})
        else:
            return JsonResponse({'result':'errorr','message':'You must log in'})

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(
            category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)

from django import forms 
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Restaurant

class RegistrationForm(forms.Form):
    name=forms.CharField()
    restaurant_address=forms.CharField()
    restaurant_phone=forms.CharField()
    restaurant_email=forms.EmailField(required=False)
    restaurant_profile=forms.ImageField(required=False)

    class Meta:
        model=Restaurant
        field=(
            'name',
            'restaurant_phone',
            'restaurant_email',
            'restaurant_address',
            'restaurant_profile',
        )        

    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        name=cleaned_data.get('name')
        restaurant_phone=cleaned_data.get('restaurant_phone')
        restaurant_address=cleaned_data.get('restaurant_address')
        restaurant_profile=cleaned_data.get('restaurant_profile')
        restaurant_email=cleaned_data.get('restaurant_email')

        print(name,restaurant_phone,restaurant_address,'rest')
        if not name and not restaurant_address and not restaurant_phone:
            raise forms.ValidationError('This field required')

class AddMenuForm(forms.Form):
    name=forms.CharField()
    ingredient=forms.CharField()
    price=forms.DecimalField()
    cuisson_time=forms.IntegerField()
    for_people=forms.IntegerField()

    def clean(self):
        cleaned_data=super(AddMenuForm,self).clean()
        name=cleaned_data.get('name')
        ingredient=cleaned_data.get('ingredient')
        price=cleaned_data.get('price')
        cuisson_time=cleaned_data.get('cuisson_time')
        for_people=cleaned_data.get('for_people')

        print(name,ingredient,price,cuisson_time,for_people,'texas')

        if not name and not ingredient and not price and not cuisson_time and not for_people :
            raise forms.ValidationError('This Field is required !')
from django import forms 
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    
    first_name=forms.CharField()
    last_name=forms.CharField()
    username=forms.CharField()
    password=forms.CharField()
    password2=forms.CharField()
    email=forms.EmailField()

    CHOICES = [
        ('male', '1'),
        ('female', '2'),
    ]
    gender=forms.ChoiceField(choices=CHOICES)
    phone=forms.CharField()
    address=forms.CharField()
    birthday=forms.DateField()

    
    # source = forms.CharField(       # A hidden input for internal use
    #     max_length=50,              # tell from which page the user sent the message
    #     widget=forms.HiddenInput()
    # )

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password=cleaned_data.get('password')
        password2=cleaned_data.get('password2')

        queryset=User.objects.filter(username__iexact=username)
        if queryset.exists():
            msg = "Username already in use"
            self.add_error("username", msg)
            raise forms.ValidationError('Username already in use!')

        if password != password2 :
            msg = "Password do not match"
            self.add_error("password", msg)
            self.add_error("password2", msg)
            raise forms.ValidationError('The password do not match!')

        
        if not first_name and not email and not last_name:
            raise forms.ValidationError('You have to write something!')
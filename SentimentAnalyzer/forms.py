from django.forms import ModelForm
from .models import Order, Client, File

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        # fields = ['Client', 'files', etc]
        fields = "__all__"

class CreateUserForm(UserCreationForm): #RegistrationForm
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']


#Forms to upload CSV file -Rownok
class MyForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["filename", "file", ]
        labels = {'filename': "File Name", "file": "File", }

        

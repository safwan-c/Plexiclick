from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from .models import User,Plexiorder
from django import forms

 
class CustomUserForm(UserCreationForm):
  username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
  email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
  password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
  password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
  class Meta:
    model=User
    fields=['username','email','password1','password2']

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)   


class MyForm(forms.Form):
    field1 = forms.CharField()
    field2 = forms.IntegerField()

    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Plexiorder
        fields=['first_name','last_name','country','address','city','zipcode','phone','notes']



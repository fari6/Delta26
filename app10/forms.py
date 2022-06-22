from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app10.models import AddCategoryModel
from app10.models import AddSubscriptionModel
 
class UserRegisterForm(UserCreationForm):
	class Meta:
		model=User
		fields=["username","first_name","last_name","password1","email"]

class AddCategoryForm(forms.ModelForm):        
    class Meta:
        model= AddCategoryModel
        fields=['name',]

class AddSubscriptionForm(forms.ModelForm):
    class Meta:
        model=AddSubscriptionModel
        fields=["name","duration","feestructure","category"]
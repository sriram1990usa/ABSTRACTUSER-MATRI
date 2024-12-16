from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, Select, SelectDateWidget, fields  
from .models import *  
from .scripts import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()   

class DateInput(forms.DateInput):
    input_type = 'date'     

class ProfileUpdateForm(forms.ModelForm):   
    class Meta:
        model = Profile
        fields = '__all__'            
        widgets = {
            'birth_date': DateInput(),
            'gender': Select(),
            # 'state': Select(choices=STATE_CHOICES),
            # 'country': Select(choices=COUNTRY_CHOICES),
        }

class AddimgUpdateForm(forms.ModelForm):
    class Meta:
        model = Addimg        
        # fields = '__all__'
        exclude = ["propic_hash"]
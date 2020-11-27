from django import forms
from .models import Login

class LoginForm(forms.ModelForm):
    username = forms.CharField      (max_length = 100, 
    required = True)
    password = forms.CharField(max_length = 100, required = True)
    
    class meta:
        model = Login
        field = [
            'username',
            'password'
        ]
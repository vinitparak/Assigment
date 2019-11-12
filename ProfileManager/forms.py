from django import forms
from .models import Users, Employee
from django.core.validators import RegexValidator


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ('email', 'password',)


class LoginForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ('email', 'password',)


class EmployeeRegistration(forms.ModelForm):
    my_validator = RegexValidator(r"\d{10}", "Phone n0. should be 10 digits")
    phone = forms.CharField(validators=[my_validator], max_length=10)
    class Meta:
        model = Employee
        fields = ('email', 'name', 'phone', 'gender', 'type', 'hobbies', 'profile_picture',)


class EmployeeLogin(forms.ModelForm):
    email = 'asdfasdf@asdf.com'
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employee
        fields = ('email', 'password')

class EmployeeData(forms.ModelForm):
    my_validator = RegexValidator(r"\d{10}", "Phone n0. should be 10 digits")
    phone = forms.CharField(validators=[my_validator], max_length=10)
    class Meta:
        model = Employee
        fields = ('email', 'name', 'phone', 'gender', 'hobbies', 'profile_picture',)
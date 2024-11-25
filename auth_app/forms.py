from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from administration.models import Staff
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm  # Import Staff model

User = get_user_model()

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Include fields you want users to edit
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),  # Example of customizing the widget
        }
class RegistrationForm(forms.ModelForm):
    staff_number = forms.CharField(max_length=100, required=True, label="Staff Number")
    role = forms.ChoiceField(choices=[('staff', 'Staff'), ('technician', 'Technician')], label="Role")

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
        
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xl',
                "placeholder": "Enter Your Username"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-xl',
                "placeholder": "Enter Your Password"
            }
        )
    )
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, label='Тип пользователя')

    class Meta:
        model = User
        fields = ['email', 'username', 'user_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
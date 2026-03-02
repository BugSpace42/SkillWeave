# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .models import User


class RegisterView(CreateView):  # FR-01
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomLoginView(LoginView):  # FR-02
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
# skillweava/views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        # Если пользователь авторизован, можно показывать ему специальную версию
        # или все равно показывать главную
        return super().dispatch(request, *args, **kwargs)
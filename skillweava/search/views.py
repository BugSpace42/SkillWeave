# search/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib import messages
from .filters import UserProfileFilter, CollaborationRequestFilter
from .models import CollaborationRequest
from profiles.models import UserProfile
from django.db.models import Q


class UserSearchView(LoginRequiredMixin, FilterView):  # FR-07, FR-08
    model = UserProfile
    filterset_class = UserProfileFilter
    template_name = 'search/user_search.html'
    context_object_name = 'profiles'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        # Исключаем пользователей без id профиля (на всякий случай)
        queryset = queryset.filter(pk__isnull=False)

        # Для HR показываем всех, для обычных пользователей - только не-HR
        if self.request.user.user_type == 'hr':
            return queryset
        return queryset.exclude(user__user_type='hr')


class CollaborationRequestListView(LoginRequiredMixin, FilterView):  # FR-09
    model = CollaborationRequest
    filterset_class = CollaborationRequestFilter
    template_name = 'search/request_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        return CollaborationRequest.objects.filter(status='active')


class CollaborationRequestCreateView(LoginRequiredMixin, CreateView):
    model = CollaborationRequest
    fields = ['title', 'description', 'required_hard_skills', 'required_soft_skills']
    template_name = 'search/request_form.html'
    success_url = reverse_lazy('search:request_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Запрос на сотрудничество успешно создан!')
        return super().form_valid(form)


class CollaborationRequestDetailView(LoginRequiredMixin, DetailView):
    model = CollaborationRequest
    template_name = 'search/request_detail.html'
    context_object_name = 'request'
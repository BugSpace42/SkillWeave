# profiles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, UpdateView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UserProfile, OnboardingResponse, Document, Skill
from .forms import OnboardingForm, UserProfileForm, DocumentForm
from accounts.models import User

class OnboardingView(LoginRequiredMixin, FormView):  # FR-03
    template_name = 'profiles/onboarding.html'
    form_class = OnboardingForm
    success_url = reverse_lazy('profiles:edit')  # Временный URL, будет переопределен

    def form_valid(self, form):
        # Сохраняем ответы онбординга
        for key, value in form.cleaned_data.items():
            OnboardingResponse.objects.create(
                user=self.request.user,
                question=form.fields[key].label,
                answer=value
            )

        # Отмечаем пользователя как прошедшего онбординг
        self.request.user.is_onboarded = True
        self.request.user.save()

        # Создаем профиль, если его нет
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)

        messages.success(self.request, 'Онбординг успешно пройден! Теперь заполните дополнительную информацию.')

        # Перенаправляем на страницу редактирования профиля
        return redirect('profiles:edit')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_onboarded:
            return redirect('profiles:edit')
        return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'


class ProfileEditView(LoginRequiredMixin, UpdateView):  # FR-04
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/edit.html'

    def get_object(self, queryset=None):
        obj, created = UserProfile.objects.get_or_create(user=self.request.user)
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return reverse_lazy('profiles:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)

class DocumentListView(LoginRequiredMixin, ListView):  # FR-05
    model = Document
    template_name = 'profiles/documents.html'
    context_object_name = 'documents'

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class DocumentUploadView(LoginRequiredMixin, CreateView):  # FR-05
    model = Document
    form_class = DocumentForm
    template_name = 'profiles/document_upload.html'
    success_url = reverse_lazy('profiles:documents')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
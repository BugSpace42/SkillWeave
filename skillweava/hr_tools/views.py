# hr_tools/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
from chat.models import ChatRoom

User = get_user_model()


class HRRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 'hr'


class CandidateSearchView(LoginRequiredMixin, HRRequiredMixin, ListView):  # FR-10
    model = UserProfile
    template_name = 'hr_tools/candidate_search.html'
    context_object_name = 'candidates'
    paginate_by = 20

    def get_queryset(self):
        queryset = UserProfile.objects.exclude(user__user_type='hr')

        # Фильтрация по навыкам
        hard_skills = self.request.GET.getlist('hard_skills')
        soft_skills = self.request.GET.getlist('soft_skills')

        if hard_skills:
            queryset = queryset.filter(hard_skills__id__in=hard_skills).distinct()

        if soft_skills:
            queryset = queryset.filter(soft_skills__id__in=soft_skills).distinct()

        # Поиск по ключевым словам
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                models.Q(first_name__icontains=keyword) |
                models.Q(last_name__icontains=keyword) |
                models.Q(specialization__icontains=keyword)
            )

        # Фильтр по репутации
        min_reputation = self.request.GET.get('min_reputation')
        if min_reputation:
            queryset = queryset.filter(user__reputation__gte=min_reputation)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from profiles.models import Skill
        context['hard_skills'] = Skill.objects.filter(skill_type='hard')
        context['soft_skills'] = Skill.objects.filter(skill_type='soft')
        return context


@login_required
def send_invitation(request, user_id):  # FR-16
    if request.user.user_type != 'hr':
        messages.error(request, 'Только HR-специалисты могут отправлять приглашения')
        return redirect('search:user_search')

    candidate = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        job_title = request.POST.get('job_title')
        company = request.user.profile.company if hasattr(request.user, 'profile') else 'Наша компания'

        # Создаем чат с кандидатом для обсуждения предложения
        chat_room = ChatRoom.objects.filter(participants=request.user).filter(participants=candidate).first()

        if not chat_room:
            chat_room = ChatRoom.objects.create()
            chat_room.participants.add(request.user, candidate)

        # Отправляем приглашение (как системное сообщение в чат)
        from chat.models import Message
        invitation_text = f"""🎯 **ПРИГЛАШЕНИЕ НА РАБОТУ**

Компания: {company}
Должность: {job_title}

Сообщение от HR:
{message}

Для обсуждения деталей, пожалуйста, ответьте в этом чате."""

        Message.objects.create(
            room=chat_room,
            sender=request.user,
            content=invitation_text
        )

        messages.success(request, f'Приглашение отправлено пользователю {candidate.email}')
        return redirect('chat:chat_room', room_id=chat_room.id)

    return render(request, 'hr_tools/send_invitation.html', {'candidate': candidate})
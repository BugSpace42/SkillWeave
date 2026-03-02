# collaboration/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils import timezone
from .models import CollaborationSession, Review
from chat.models import ChatRoom
from django.contrib.auth import get_user_model

User = get_user_model()


class SessionListView(LoginRequiredMixin, ListView):
    model = CollaborationSession
    template_name = 'collaboration/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return CollaborationSession.objects.filter(
            models.Q(initiator=self.request.user) |
            models.Q(partner=self.request.user)
        ).order_by('-created_at')


class SessionDetailView(LoginRequiredMixin, DetailView):
    model = CollaborationSession
    template_name = 'collaboration/session_detail.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(session=self.object)
        context['user_review'] = Review.objects.filter(
            session=self.object,
            reviewer=self.request.user
        ).first()
        return context


@login_required
def create_session(request, user_id):  # FR-13
    partner = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Создаем чат-комнату для сессии
        chat_room = ChatRoom.objects.create()
        chat_room.participants.add(request.user, partner)

        # Создаем сессию сотрудничества
        session = CollaborationSession.objects.create(
            title=title,
            description=description,
            initiator=request.user,
            partner=partner,
            chat_room=chat_room,
            status='pending'
        )

        messages.success(request, 'Запрос на сотрудничество отправлен!')
        return redirect('collaboration:session_detail', pk=session.id)

    return render(request, 'collaboration/create_session.html', {'partner': partner})


@login_required
def complete_session(request, pk):  # FR-13, FR-14
    session = get_object_or_404(CollaborationSession, id=pk)

    if request.user not in [session.initiator, session.partner]:
        messages.error(request, 'У вас нет прав для завершения этой сессии')
        return redirect('collaboration:session_detail', pk=session.id)

    if request.method == 'POST':
        session.status = 'completed'
        session.end_date = timezone.now()
        session.save()

        # Повышаем рейтинг
        session.initiator.reputation += 10
        session.partner.reputation += 10
        session.initiator.save()
        session.partner.save()

        messages.success(request, 'Сессия успешно завершена!')
        return redirect('collaboration:session_detail', pk=session.id)

    return render(request, 'collaboration/complete_session.html', {'session': session})


@login_required
def create_review(request, pk):  # FR-15
    session = get_object_or_404(CollaborationSession, id=pk)

    if request.user not in [session.initiator, session.partner]:
        messages.error(request, 'Вы не участвовали в этой сессии')
        return redirect('collaboration:session_detail', pk=session.id)

    if session.status != 'completed':
        messages.error(request, 'Нельзя оставить отзыв до завершения сессии')
        return redirect('collaboration:session_detail', pk=session.id)

    existing_review = Review.objects.filter(session=session, reviewer=request.user).first()
    if existing_review:
        messages.error(request, 'Вы уже оставили отзыв')
        return redirect('collaboration:session_detail', pk=session.id)

    reviewed = session.partner if request.user == session.initiator else session.initiator

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            session=session,
            reviewer=request.user,
            reviewed=reviewed,
            rating=rating,
            comment=comment
        )

        messages.success(request, 'Отзыв успешно добавлен!')
        return redirect('collaboration:session_detail', pk=session.id)

    return render(request, 'collaboration/create_review.html', {'session': session, 'reviewed': reviewed})
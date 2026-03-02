# chat/views.py
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.conf import settings
from .models import ChatRoom, Message, CallSession
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatListView(LoginRequiredMixin, ListView):  # FR-11
    model = ChatRoom
    template_name = 'chat/chat_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user)


class ChatRoomView(LoginRequiredMixin, DetailView):  # FR-11
    model = ChatRoom
    template_name = 'chat/chat_room.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(room=self.object)
        context['other_user'] = self.object.participants.exclude(id=self.request.user.id).first()
        return context


@login_required
def get_or_create_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    room = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not room:
        room = ChatRoom.objects.create()
        room.participants.add(request.user, other_user)

    return redirect('chat:chat_room', room_id=room.id)


@login_required
def start_call(request, room_id):  # FR-12
    room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
    call_type = request.POST.get('call_type', 'video')

    # Create Jitsi room name
    jitsi_room = f"skillweava_{uuid.uuid4().hex[:8]}"

    call = CallSession.objects.create(
        room=room,
        initiator=request.user,
        call_type=call_type,
        jitsi_room_name=jitsi_room
    )

    return JsonResponse({
        'call_id': call.id,
        'jitsi_room': jitsi_room,
        'jitsi_domain': settings.JITSI_DOMAIN
    })


@login_required
def call_detail(request, call_id):  # FR-12, FR-17
    call = get_object_or_404(CallSession, id=call_id, room__participants=request.user)
    return render(request, 'chat/call.html', {
        'call': call,
        'jitsi_domain': settings.JITSI_DOMAIN
    })
# chat/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):  # FR-11
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Чат-комната'
        verbose_name_plural = 'Чат-комнаты'

    def __str__(self):
        return f"Chat {self.id}"


class Message(models.Model):  # FR-11
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"


class CallSession(models.Model):  # FR-12
    CALL_TYPE_CHOICES = (
        ('audio', 'Аудиозвонок'),
        ('video', 'Видеозвонок'),
    )

    STATUS_CHOICES = (
        ('initiated', 'Инициирован'),
        ('active', 'Активен'),
        ('ended', 'Завершен'),
        ('missed', 'Пропущен'),
    )

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='calls')
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_calls')
    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    jitsi_room_name = models.CharField(max_length=255, unique=True)  # FR-17
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сессия звонка'
        verbose_name_plural = 'Сессии звонков'
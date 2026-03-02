# collaboration/models.py
from django.db import models
from django.contrib.auth import get_user_model
from chat.models import ChatRoom

User = get_user_model()


class CollaborationSession(models.Model):  # FR-13
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('active', 'Активна'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_sessions')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participating_sessions')
    chat_room = models.OneToOneField(ChatRoom, on_delete=models.CASCADE, related_name='collaboration_session')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Сессия сотрудничества'
        verbose_name_plural = 'Сессии сотрудничества'

    def __str__(self):
        return self.title

    def complete(self):  # FR-14
        self.status = 'completed'
        self.save()

        # Повышаем рейтинг обоим пользователям
        self.initiator.reputation += 10
        self.partner.reputation += 10
        self.initiator.save()
        self.partner.save()


class Review(models.Model):  # FR-15
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    session = models.ForeignKey(CollaborationSession, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session', 'reviewer', 'reviewed']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.reviewer} для {self.reviewed}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Обновляем репутацию пользователя
        user = self.reviewed
        reviews = Review.objects.filter(reviewed=user)
        avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        user.reputation = avg_rating * 20  # Преобразуем в шкалу 0-100
        user.save()
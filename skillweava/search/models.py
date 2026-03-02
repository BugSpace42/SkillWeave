# search/models.py
from django.db import models
from django.contrib.auth import get_user_model
from profiles.models import Skill

User = get_user_model()


class CollaborationRequest(models.Model):  # FR-09
    STATUS_CHOICES = (
        ('active', 'Активный'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaboration_requests')
    required_hard_skills = models.ManyToManyField(Skill, related_name='required_for_requests',
                                                  limit_choices_to={'skill_type': 'hard'})
    required_soft_skills = models.ManyToManyField(Skill, related_name='required_for_requests_soft',
                                                  limit_choices_to={'skill_type': 'soft'}, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Запрос на сотрудничество'
        verbose_name_plural = 'Запросы на сотрудничество'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
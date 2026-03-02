# profiles/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


class Skill(models.Model):
    SKILL_TYPE_CHOICES = (
        ('hard', 'Hard Skill'),
        ('soft', 'Soft Skill'),
    )

    name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPE_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return f"{self.name} ({self.get_skill_type_display()})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # FR-04: Дополнительная информация
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True, verbose_name='Текущая компания')
    position = models.CharField(max_length=200, blank=True, verbose_name='Должность')
    experience_years = models.IntegerField(default=0, verbose_name='Лет опыта')

    # FR-05: Документы
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        verbose_name='Резюме'
    )

    # FR-06: Промо-ролик
    promo_video_url = models.URLField(blank=True, verbose_name='Ссылка на промо-ролик')

    # Навыки пользователя
    hard_skills = models.ManyToManyField(Skill, related_name='users_hard', blank=True,
                                         limit_choices_to={'skill_type': 'hard'})
    soft_skills = models.ManyToManyField(Skill, related_name='users_soft', blank=True,
                                         limit_choices_to={'skill_type': 'soft'})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.user.username

    def __str__(self):
        return f"Профиль {self.user.email}"


class OnboardingResponse(models.Model):  # FR-03
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    answer = models.TextField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ответ онбординга'
        verbose_name_plural = 'Ответы онбординга'


class Document(models.Model):  # FR-05
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
# search/filters.py
import django_filters
from django.db.models import Q
from profiles.models import UserProfile
from .models import CollaborationRequest


class UserProfileFilter(django_filters.FilterSet):  # FR-07, FR-08, FR-10
    keyword = django_filters.CharFilter(method='filter_by_keyword', label='Поиск по ключевым словам')
    hard_skills = django_filters.ModelMultipleChoiceFilter(
        field_name='hard_skills',
        queryset=UserProfile.hard_skills.field.related_model.objects.filter(skill_type='hard'),
        label='Hard Skills'
    )
    soft_skills = django_filters.ModelMultipleChoiceFilter(
        field_name='soft_skills',
        queryset=UserProfile.soft_skills.field.related_model.objects.filter(skill_type='soft'),
        label='Soft Skills'
    )
    min_reputation = django_filters.NumberFilter(field_name='user__reputation', lookup_expr='gte',
                                                 label='Мин. репутация')
    specialization = django_filters.CharFilter(lookup_expr='icontains', label='Специализация')

    class Meta:
        model = UserProfile
        fields = ['specialization', 'hard_skills', 'soft_skills']

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(specialization__icontains=value) |
            Q(bio__icontains=value)
        )


class CollaborationRequestFilter(django_filters.FilterSet):  # FR-09
    hard_skills = django_filters.ModelMultipleChoiceFilter(
        field_name='required_hard_skills',
        queryset=CollaborationRequest.required_hard_skills.field.related_model.objects.filter(skill_type='hard'),
        label='Hard Skills'
    )
    soft_skills = django_filters.ModelMultipleChoiceFilter(
        field_name='required_soft_skills',
        queryset=CollaborationRequest.required_soft_skills.field.related_model.objects.filter(skill_type='soft'),
        label='Soft Skills'
    )

    class Meta:
        model = CollaborationRequest
        fields = ['status', 'hard_skills', 'soft_skills']
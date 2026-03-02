# profiles/forms.py
from django import forms
from .models import UserProfile, Document

class OnboardingForm(forms.Form):  # FR-03
    question_1 = forms.CharField(
        label='Какие у вас Hard Skills? (перечислите через запятую)',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    )
    question_2 = forms.CharField(
        label='Какие у вас Soft Skills? (перечислите через запятую)',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    )
    question_3 = forms.CharField(
        label='Расскажите о своем опыте работы',
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True
    )
    question_4 = forms.CharField(
        label='Чего вы хотите достичь на платформе?',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    )

class UserProfileForm(forms.ModelForm):  # FR-04
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'specialization', 'bio',
            'phone', 'location', 'company', 'position', 'experience_years',
            'avatar', 'promo_video_url', 'hard_skills', 'soft_skills'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'hard_skills': forms.CheckboxSelectMultiple(),
            'soft_skills': forms.CheckboxSelectMultiple(),
        }

class DocumentForm(forms.ModelForm):  # FR-05
    class Meta:
        model = Document
        fields = ['title', 'file']
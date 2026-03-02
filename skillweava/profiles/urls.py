# profiles/urls.py
from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('onboarding/', views.OnboardingView.as_view(), name='onboarding'),  # FR-03
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='detail'),  # FR-04
    path('profile/edit/', views.ProfileEditView.as_view(), name='edit'),  # FR-04
    path('documents/', views.DocumentListView.as_view(), name='documents'),  # FR-05
    path('documents/upload/', views.DocumentUploadView.as_view(), name='document_upload'),  # FR-05
]
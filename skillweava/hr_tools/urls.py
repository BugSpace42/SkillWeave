# hr_tools/urls.py
from django.urls import path
from . import views

app_name = 'hr_tools'

urlpatterns = [
    path('candidates/', views.CandidateSearchView.as_view(), name='candidate_search'),  # FR-10
    path('invite/<int:user_id>/', views.send_invitation, name='send_invitation'),  # FR-16
]
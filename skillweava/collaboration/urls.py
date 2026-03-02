# collaboration/urls.py
from django.urls import path
from . import views

app_name = 'collaboration'

urlpatterns = [
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('sessions/create/<int:user_id>/', views.create_session, name='create_session'),  # FR-13
    path('sessions/<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('sessions/<int:pk>/complete/', views.complete_session, name='complete_session'),  # FR-13, FR-14
    path('sessions/<int:pk>/review/', views.create_review, name='create_review'),  # FR-15
]
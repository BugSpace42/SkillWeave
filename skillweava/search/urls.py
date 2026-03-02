# search/urls.py
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('users/', views.UserSearchView.as_view(), name='user_search'),  # FR-07, FR-08
    path('requests/', views.CollaborationRequestListView.as_view(), name='request_list'),  # FR-09
    path('requests/create/', views.CollaborationRequestCreateView.as_view(), name='request_create'),
    path('requests/<int:pk>/', views.CollaborationRequestDetailView.as_view(), name='request_detail'),
]
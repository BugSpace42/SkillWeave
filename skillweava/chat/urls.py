# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='chat_list'),  # FR-11
    path('room/<int:user_id>/', views.get_or_create_room, name='get_or_create_room'),
    path('room/<int:room_id>/', views.ChatRoomView.as_view(), name='chat_room'),  # FR-11
    path('call/start/<int:room_id>/', views.start_call, name='start_call'),  # FR-12
    path('call/<int:call_id>/', views.call_detail, name='call_detail'),  # FR-12, FR-17
]
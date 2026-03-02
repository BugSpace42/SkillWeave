# skillweava/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Импортируем views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # Теперь главная страница ведет на HomeView
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('search/', include('search.urls')),
    path('chat/', include('chat.urls')),
    path('collaboration/', include('collaboration.urls')),
    path('hr/', include('hr_tools.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
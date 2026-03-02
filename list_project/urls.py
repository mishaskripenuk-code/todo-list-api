
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.models import User
from django.http import HttpResponse

def create_superuser_view(request):
    try:
        if not User.objects.filter(username='myadmin').exists():
            User.objects.create_superuser('myadmin', 'admin@example.com', 'password123')
            return HttpResponse("✅ Суперкористувача створено! Логін: myadmin, Пароль: password123")
        else:
            return HttpResponse("⚠️ Користувач 'myadmin' вже існує.")
    except Exception as e:
        return HttpResponse(f"❌ Помилка: {str(e)}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')), # Твій існуючий шлях
    # 👇 ДОДАЙ ЦЕЙ РЯДОК (це адреса "кнопки")
    path('secret-admin-create/', create_superuser_view),
]
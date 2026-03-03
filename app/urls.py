from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView


router = DefaultRouter()


router.register(r'todos', TodoViewSet, basename='todo')


urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    # Головна сторінка (список)
    path('', TaskList.as_view(), name='tasks'),
    
    # Операції із завданнями
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]
from rest_framework import viewsets, permissions 
from .models import Todo
from .serializers import TodoSerializer
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    
    permission_classes = [permissions.IsAuthenticated]

    
    def get_queryset(self):
        
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
       # --- ЛОГІКА ВЕБ-САЙТУ ---

# 1. Вхід у систему
class CustomLoginView(LoginView):
    template_name = 'task_login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

# 2. Реєстрація
class RegisterPage(FormView):
    template_name = 'task_register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

# 3. Список завдань (Тільки мої!)
class TaskList(LoginRequiredMixin, ListView):
    model = Todo   # 👈 Змінив Task на Todo
    context_object_name = 'tasks'
    template_name = 'task_list.html'

    def get_queryset(self):
        # 👇 ЯВНИЙ пошук: "Дай мені всі Todo, де user - це я"
        return Todo.objects.filter(owner=self.request.user)
    
# 4. Створення завдання
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Todo   # 👈 Змінив Task на Todo
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')
    template_name = 'task_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(TaskCreate, self).form_valid(form)

# 5. Редагування
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Todo   # 👈 Змінив Task на Todo
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')
    template_name = 'task_form.html'

# 6. Видалення
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Todo   # 👈 Змінив Task на Todo
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task_confirm_delete.html'
# todo/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Task, Category
from .forms import TaskForm, CategoryForm


# ─── TASK LIST VIEW ────────────────────────────────────────────────────────────

class TaskListView(ListView):
    """List all tasks — home page."""
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        """Filter and search support."""
        queryset = Task.objects.all()
        
        # Filter by completion status
        status = self.request.GET.get('status')
        if status == 'completed':
            queryset = queryset.filter(completed=True)
        elif status == 'pending':
            queryset = queryset.filter(completed=False)
        
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority in ['low', 'medium', 'high']:
            queryset = queryset.filter(priority=priority)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Extra context for the template."""
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.count()
        context['completed_tasks'] = Task.objects.filter(completed=True).count()
        context['pending_tasks'] = Task.objects.filter(completed=False).count()
        return context


# ─── TASK CREATE VIEW ──────────────────────────────────────────────────────────

class TaskCreateView(CreateView):
    """Create a new task."""
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:task_list')
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Task added successfully.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add new task'
        context['button_text'] = 'Add task'
        return context


# ─── TASK UPDATE VIEW ──────────────────────────────────────────────────────────

class TaskUpdateView(UpdateView):
    """Edit an existing task."""
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:task_list')
    
    def form_valid(self, form):
        messages.success(self.request, '✏️ Task updated successfully.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit task'
        context['button_text'] = 'Update'
        return context


# ─── TASK DELETE VIEW ──────────────────────────────────────────────────────────

class TaskDeleteView(DeleteView):
    """Delete a task."""
    model = Task
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('todo:task_list')
    
    def form_valid(self, form):
        messages.success(self.request, '🗑️ Task deleted successfully.')
        return super().form_valid(form)


# ─── TOGGLE COMPLETE ───────────────────────────────────────────────────────────

class TaskToggleView(View):
    """Toggle task complete / incomplete."""
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.completed = not task.completed
        task.save()
        status = "complete" if task.completed else "incomplete"
        messages.info(request, f'Task "{task.title}" marked as {status}.')
        return redirect('todo:task_list')
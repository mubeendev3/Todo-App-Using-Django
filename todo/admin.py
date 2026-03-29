from django.contrib import admin
from .models import Task, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'completed', 'category', 'created_at']
    list_filter = ['completed', 'priority', 'category']
    search_fields = ['title', 'description']
    list_editable = ['completed']  # Edit completion status from the list
    date_hierarchy = 'created_at'
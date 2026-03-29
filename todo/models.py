# todo/models.py

from django.db import models


class Category(models.Model):
    """Task categories such as Work, Personal, Shopping."""
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Task(models.Model):
    """Main To-Do task model"""
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    title = models.CharField(max_length=200)               # Task title
    description = models.TextField(blank=True, null=True)  # Optional detail
    completed = models.BooleanField(default=False)         # Whether the task is done
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)   # Set when created
    updated_at = models.DateTimeField(auto_now=True)       # Updated on each save
    due_date = models.DateField(null=True, blank=True)     # Optional deadline
    
    class Meta:
        ordering = ['-created_at']  # Newest tasks first
    
    def __str__(self):
        return self.title
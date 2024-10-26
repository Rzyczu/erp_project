from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import os
import random, string

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    identifier = models.CharField(max_length=6, unique=True, default='')

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TeamUserRole(models.Model):
    ROLE_CHOICES = [
            ('project_manager', 'Project Manager'),  # Project Manager is still special
        ('tester', 'Tester'),
        ('frontend_developer', 'Frontend Developer'),
        ('backend_developer', 'Backend Developer'),
        ('fullstack_developer', 'Fullstack Developer'),
        ('devops', 'DevOps Engineer'),
        ('data_scientist', 'Data Scientist'),
        ('qa_engineer', 'QA Engineer'),
        ('designer', 'Designer'),
        ('ui_ux_designer', 'UI/UX Designer'),
        ('scrum_master', 'Scrum Master'),
        ('business_analyst', 'Business Analyst'),
        ('product_owner', 'Product Owner'),
        ('technical_lead', 'Technical Lead'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('team', 'user')

    def clean(self):
        if self.role == 'project_manager':
            if TeamUserRole.objects.filter(team=self.team, role='project_manager').exclude(id=self.id).exists():
                raise ValidationError("Each team can have only one Project Manager.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    def clean(self):
        # Ensure only one project manager per team
        if self.role == 'project_manager' and TeamUserRole.objects.filter(team=self.team, role='project_manager').exclude(id=self.id).exists():
            raise ValidationError("Each team can have only one Project Manager.")
        
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    images = models.ImageField(upload_to='static/images/tasks', null=True, blank=True)
    milestones = models.JSONField(null=True, blank=True)  # JSON field for storing milestones

    def __str__(self):
        return self.name
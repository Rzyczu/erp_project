from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='teams', blank=True)  # Keep this field temporarily
    team_users = models.ManyToManyField(User, through='TeamUserRole', related_name='team_roles', blank=True)  # New field
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
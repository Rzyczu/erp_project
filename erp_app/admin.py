from django.contrib import admin
from .models import Team  # Import other models as needed

from django.contrib.auth.models import User

# Register the models
admin.site.register(Team)

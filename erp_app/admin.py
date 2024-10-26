from django.contrib import admin
from .models import *

from django.contrib.auth.models import User

# Register the models
admin.site.register(Task)

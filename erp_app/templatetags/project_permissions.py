# In templatetags/project_permissions.py

from django import template
from ..models import TeamUserRole

register = template.Library()

@register.simple_tag
def is_project_manager(user, team_id):
    """Returns True if the user is a project manager of the specified team."""
    return TeamUserRole.objects.filter(user=user, team_id=team_id, role='project_manager').exists()

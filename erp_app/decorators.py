from django.core.exceptions import PermissionDenied
from .models import TeamUserRole, Team

def project_manager_required(view_func):
    """Decorator to check if the user is a project manager for the specified team."""
    def _wrapped_view(request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        if team_id:
            is_pm = TeamUserRole.objects.filter(user=request.user, team_id=team_id, role='project_manager').exists()
            if is_pm:
                return view_func(request, *args, **kwargs)
        raise PermissionDenied  # Return 403 if user is not a project manager
    return _wrapped_view

# In context_processors.py

from .models import TeamUserRole

def is_project_manager(request):
    def check_pm(team_id):
        """Returns True if the request user is a project manager of the specified team."""
        if request.user.is_authenticated:
            return TeamUserRole.objects.filter(user=request.user, team_id=team_id, role='project_manager').exists()
        return False
    return {'is_project_manager': check_pm}

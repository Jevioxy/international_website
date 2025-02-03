from .models import ActionHistory

def log_action(user, action_type, model_name, details):
    ActionHistory.objects.create(
        user=user,
        action_type=action_type,
        model_name=model_name,
        details=details
    )
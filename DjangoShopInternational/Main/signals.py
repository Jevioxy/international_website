from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import ActionHistory

def get_user_from_request():
    """Функция для получения текущего пользователя из запроса."""
    from threading import current_thread
    return getattr(current_thread(), 'current_user', None)

# Сигнал для создания и обновления
@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    if sender == ActionHistory:  # Избегаем записи самой модели ActionHistory
        return

    action_type = 'create' if created else 'update'
    user = get_user_from_request()

    ActionHistory.objects.create(
        user=user,
        action_type=action_type,
        model_name=sender.__name__,
        details=f'{action_type.capitalize()} record with ID {instance.pk}'
    )

# Сигнал для удаления
@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender == ActionHistory:  # Избегаем записи самой модели ActionHistory
        return

    user = get_user_from_request()

    ActionHistory.objects.create(
        user=user,
        action_type='delete',
        model_name=sender.__name__,
        details=f'Deleted record with ID {instance.pk}'
    )

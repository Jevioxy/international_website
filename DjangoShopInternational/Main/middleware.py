from threading import current_thread

class UserLoggingMiddleware:
    """Middleware для записи текущего пользователя в поток."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_thread().current_user = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        current_thread().current_user = None  # Очищаем после завершения запроса
        return response

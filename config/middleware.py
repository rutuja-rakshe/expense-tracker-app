import time
import logging
import uuid

logger = logging.getLogger('apps')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())[:8]
        request.request_id = request_id
        start = time.time()

        response = self.get_response(request)

        duration_ms = round((time.time() - start) * 1000, 2)
        user = getattr(request, 'user', None)
        user_id = user.id if user and user.is_authenticated else 'anon'

        logger.info(
            f"[{request_id}] {request.method} {request.path} "
            f"→ {response.status_code} | {duration_ms}ms | user={user_id}"
        )
        response['X-Request-ID'] = request_id
        return response
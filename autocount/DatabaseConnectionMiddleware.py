# middlewares/reconnect_middleware.py

import time
from django.db import connection, OperationalError
from django.conf import settings

class ReconnectMiddleware:
    """
    Middleware to catch broken database connection and attempt to reconnect.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        max_retries = getattr(settings, 'DB_RECONNECT_RETRIES', 3)  # Configure number of retries
        attempt = 0
        while attempt < max_retries:
            try:
                print("Reconnect DB Trying >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                response = self.get_response(request)
                return response
            except OperationalError as e:
                print(e)
                print(f"tried {attempt+1} LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                attempt += 1
                time.sleep(1)  # Short delay before retry
                connection.close()  # Close and reset the database connection
                if attempt == max_retries:
                    raise

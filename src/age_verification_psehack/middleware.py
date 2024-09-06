import time

from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.conf import settings
from .settings import COOKIE_NAME
from .models import Token

class AgeVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.age_verification_paths = settings.AGE_VERIFICATION_PATHS
        # TODO: start the proof verification server.

    def __call__(self, request):
        if request.path.startswith("/age-proof"):
            print("age-proof detected")
            # override `urlconf` so that this app's view is called. 
            request.urlconf = "age_verification_psehack.urls"
        
        elif any(request.path.startswith(path) for path in self.age_verification_paths):
            is_token_valid = False

            if COOKIE_NAME in request.COOKIES:
                token_uuid = request.COOKIES[COOKIE_NAME]
                try:
                    token = Token.objects.get(uuid=token_uuid)
                except Token.DoesNotExist:
                    token = None

                if (token is not None) and (int(token.expiration_unixtime) > int(time.time())):
                    # The token was found in the db and it was not expired.
                    is_token_valid = True

            if not is_token_valid:
                age_proof_endpoint = "/age-proof" + ("/" if settings.APPEND_SLASH else "")
                return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Age verification</title>
</head>
<body>
    <h1>Verify your age</h1>
    <script>var age_proof_endpoint = '"""+age_proof_endpoint+"""'</script>
    <script type="module" src="/static/age_verification_psehack/main.js"></script>
</body>
</html>
                            """)

        # Continue processing the request
        response = self.get_response(request)
        return response

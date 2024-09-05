import time

from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.conf import settings
from .db import TokenDB
from .settings import COOKIE_NAME

class AgeVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.age_verification_paths = settings.AGE_VERIFICATION_PATHS
        # Start the verification server.

    def __call__(self, request):
        print("request is")
        print(request)

        if request.path.startswith("/age-proof"):
            print("age-proof detected")
            # override `urlconf` so that this app's view is called. 
            request.urlconf = "age_verification_psehack.urls"
        
        elif any(request.path.startswith(path) for path in self.age_verification_paths):
            is_token_valid = False

            if COOKIE_NAME in request.COOKIES:
                token_uuid = request.COOKIES[COOKIE_NAME]
                token = TokenDB.get_or_none(TokenDB.uuid == token_uuid)

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
    <p>QR code displayed here</p>
    <script>
            // Receive proof data via ws from the mobile app.
            // POST proof data to the /age-proof endpoint
            const data = {
                proof: 'dummyProof',
                data: 'dummyData'
            };
                                
            fetch('"""+age_proof_endpoint+"""', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(data => {
                console.log('Success:', data); // Handle the response data
                // if successful, the server has set the needed cookie, so we just reload the
                // protected page
                location.reload()
            })
            .catch((error) => {
                console.error('Error:', error); // Handle any errors
            });
                                
    </script>
</body>
</html>
                            """)

        # Continue processing the request
        response = self.get_response(request)
        return response

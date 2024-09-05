import json
import uuid
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views import View
from .settings import COOKIE_NAME, TOKEN_LIFETIME
from .db import TokenDB


class AgeProofView(View):
    def post(self, request):
        # Extract the proof data from the POST body
        raw_body = request.body
        data = json.loads(raw_body)

        print("endpoint got data", data)


        # TODO: get verification result from an external verifier
        verification_success = True # or False

        if not verification_success:
            return HttpResponseForbidden("Proof verification failed")
        else:
            uuid4 = str(uuid.uuid4())

            response = HttpResponse("Verification successful")
            response.set_cookie(COOKIE_NAME, uuid4, max_age=TOKEN_LIFETIME)
            
            ret = TokenDB(uuid=uuid4, expiration_unixtime=int(time.time()) + TOKEN_LIFETIME).save()
            print("TokenDB returned after save", ret)

            return response



        

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('age-proof/', csrf_exempt(views.AgeProofView.as_view()), name='age_proof_view'),
]
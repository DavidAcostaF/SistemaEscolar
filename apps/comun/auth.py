# apps/common/auth.py
from ninja.security import HttpBearer
from django.conf import settings

class APIKeyAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == settings.API_KEY:  
            return token
        return None

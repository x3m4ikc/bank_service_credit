import os

import requests
from django.contrib.auth.middleware import AuthenticationMiddleware, get_user
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from dotenv import load_dotenv
from rest_framework import status

load_dotenv()


class CreditAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        url = str(os.getenv("URL_AUTH"))
        request.user = SimpleLazyObject(lambda: get_user(request))
        try:
            data = {"access_token": request.META["HTTP_AUTHORIZATION"]}
        except KeyError:
            request.user = AnonymousUser()
        else:
            response = requests.Session().post(url=url, data=data)
            if response.status_code != status.HTTP_200_OK:
                request.user = AnonymousUser()
            else:
                request.user = User()


class User(AnonymousUser):
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

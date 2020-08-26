from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from ..const import TOKEN_BLACKLIST, TOKEN_EXPIRED, TOKEN_INVALID, AUTHENTICATION_METHOD
from ..utils import decode_auth_token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or len(auth) == 1 or len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header')
        return self.__authenticate_token(auth[1].decode())

    def authenticate_header(self, request):
        return AUTHENTICATION_METHOD

    @staticmethod
    def __authenticate_token(token):
        user_id = decode_auth_token(token)
        if not user_id or user_id == TOKEN_INVALID:
            raise exceptions.AuthenticationFailed('Invalid token. Please log in again.')
        elif user_id == TOKEN_EXPIRED:
            raise exceptions.AuthenticationFailed('Signature expired. Please log in again.')
        elif user_id == TOKEN_BLACKLIST:
            raise exceptions.AuthenticationFailed('Token blacklisted. Please log in again.')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not exist.')

        return user, token

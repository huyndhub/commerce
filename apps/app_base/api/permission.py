from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from apps.personal.models import Account
from apps.personal.const import TOKEN_BLACKLIST, TOKEN_EXPIRED, TOKEN_INVALID

from ..const import AUTHENTICATION_METHOD


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
        account_id = Account.decode_auth_token(token)
        if not account_id or account_id == TOKEN_INVALID:
            raise exceptions.AuthenticationFailed('Invalid token. Please log in again.')
        elif account_id == TOKEN_EXPIRED:
            raise exceptions.AuthenticationFailed('Signature expired. Please log in again.')
        elif account_id == TOKEN_BLACKLIST:
            raise exceptions.AuthenticationFailed('Token blacklisted. Please log in again.')

        try:
            account = Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            raise exceptions.AuthenticationFailed('Account not exist.')

        return account, token

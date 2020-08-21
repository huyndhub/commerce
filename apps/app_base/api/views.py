from rest_framework import exceptions
from rest_framework.views import APIView

from apps.personal.models import Account, BlacklistToken

from ..utils import decrypt
from .permission import TokenAuthentication
from .response import SuccessResponse


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            account = Account.objects.get(username=username)
            password_decrypt = decrypt(account.password)
            if password != password_decrypt:
                raise exceptions.AuthenticationFailed('Invalid password.')
        except Account.DoesNotExist:
            raise exceptions.NotFound('Not found username.')

        jwt_token = Account.encode_auth_token(account.pk)
        return SuccessResponse(message='Login success.', data={'token': jwt_token})


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        try:
            BlacklistToken.objects.create(token=request.auth, account_id=request.user.id)
            return SuccessResponse(message='Logout success.')
        except Exception as e:
            print(e)
            raise exceptions.APIException

from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView

from apps.app_base.api.response import SuccessResponse

from ..models import UserInfo, BlacklistToken
from ..utils import encode_auth_token
from .permission import TokenAuthentication
from .serializers import UserInfoSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise exceptions.AuthenticationFailed('Invalid password.')
        except User.DoesNotExist:
            raise exceptions.NotFound('Not found username.')

        jwt_token = encode_auth_token(user.pk)
        return SuccessResponse(message='Login success.', data={'token': jwt_token})


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        try:
            BlacklistToken.objects.create(token=request.auth, user_id=request.user.id)
            return SuccessResponse(message='Logout success.')
        except Exception as e:
            print(e)
            raise exceptions.APIException


class ListCreateView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication, )
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

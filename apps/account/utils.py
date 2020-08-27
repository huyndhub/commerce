import datetime
import jwt

from rest_framework import exceptions

from commerce.settings.common import JWT_DAYS_DELTA, JWT_SECONDS_DELTA, JWT_SECRET_KEY, JWT_ALGORITHM

from .const import TOKEN_BLACKLIST, TOKEN_EXPIRED, TOKEN_INVALID
from .models import BlacklistToken


def encode_auth_token(pk):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_DAYS_DELTA, seconds=JWT_SECONDS_DELTA),
            'iat': datetime.datetime.utcnow(),
            'user': pk,
        }
        return jwt.encode(
            payload=payload,
            key=JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )
    except Exception as e:
        print(e)
        raise exceptions.APIException('Generate token error!')


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, JWT_SECRET_KEY)
        user = payload.get('user')
        is_blacklisted_token = BlacklistToken.check_blacklist(user, auth_token) if user else False
        return TOKEN_BLACKLIST if is_blacklisted_token else user
    except jwt.ExpiredSignatureError:
        return TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return TOKEN_INVALID

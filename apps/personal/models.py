import datetime
import jwt

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import exceptions

from apps.app_base.validators import validate_email_field, validate_image_size, validate_file_extension_image
from apps.app_base.utils import decrypt, encrypt
from apps.app_base.models import base_upload
from commerce.settings.common import JWT_DAYS_DELTA, JWT_SECONDS_DELTA, JWT_SECRET_KEY, JWT_ALGORITHM, MAX_FILE_SIZE

from .const import *


def upload_avatar_path(instance, filename):
    return base_upload(filename, "personal/images")


class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'tbl_account'
        indexes = [
            models.Index(fields=('username', ))
        ]

    def save(self, *args, **kwargs):
        encrypt_pass = encrypt(self.password)
        self.password = encrypt_pass
        super(Account, self).save(*args, **kwargs)

    @staticmethod
    def encode_auth_token(pk):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_DAYS_DELTA, seconds=JWT_SECONDS_DELTA),
                'iat': datetime.datetime.utcnow(),
                'account': pk,
            }
            return jwt.encode(
                payload=payload,
                key=JWT_SECRET_KEY,
                algorithm=JWT_ALGORITHM
            )
        except Exception as e:
            print(e)
            raise exceptions.APIException('Generate token error!')

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, JWT_SECRET_KEY)
            account = payload.get('account')
            is_blacklisted_token = BlacklistToken.check_blacklist(account, auth_token) if account else False
            return TOKEN_BLACKLIST if is_blacklisted_token else account
        except jwt.ExpiredSignatureError:
            return TOKEN_EXPIRED
        except jwt.InvalidTokenError:
            return TOKEN_INVALID


class Personal(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Họ tên")
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True, blank=True,
                               validators=[validate_image_size, validate_file_extension_image],
                               verbose_name="Ảnh đại diện",
                               help_text="File upload có định dạng image và có dung lượng nhỏ hơn %sMB" % MAX_FILE_SIZE)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True, verbose_name="Giới tính")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Ngày tháng năm sinh')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name="Địa chỉ")
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True, blank=True,
        verbose_name="Vĩ độ / latitude"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True, blank=True,
        verbose_name="Kinh độ / longitude"
    )
    extra_info = models.TextField(null=True, blank=True, verbose_name="Thông tin mở rộng")
    email = models.CharField(max_length=200, null=True, blank=True, unique=True,
                             verbose_name="Email",
                             validators=[validate_email_field])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        verbose_name='Account'
    )

    class Meta:
        db_table = 'tbl_personal'
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def __str__(self):
        if self.full_name:
            return decrypt(self.full_name) or '-'
        return "-"


class BlacklistToken(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    token = models.TextField()
    blacklisted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_blacklist_token'
        verbose_name = "Blacklist Token"
        verbose_name_plural = "Blacklist Token"

    @staticmethod
    def check_blacklist(account_id, auth_token):
        is_blacklist = BlacklistToken.objects.filter(account_id=account_id, token=auth_token).first()
        return True if is_blacklist else False

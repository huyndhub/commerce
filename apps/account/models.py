from django.db import models
from django.contrib.auth.models import User

from apps.app_base.validators import validate_image_size, validate_file_extension_image
from apps.app_base.models import base_upload
from commerce.settings.common import MAX_FILE_SIZE

from .const import GENDER


def upload_avatar_path(instance, filename):
    return base_upload(filename, "account/images")


class UserInfo(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Họ tên")
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True, blank=True,
                               validators=[validate_image_size, validate_file_extension_image],
                               verbose_name="Ảnh đại diện",
                               help_text="File upload có định dạng image và có dung lượng nhỏ hơn %sMB" % MAX_FILE_SIZE)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True, verbose_name="Giới tính")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày tháng năm sinh")
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name="Địa chỉ")
    extra_info = models.TextField(null=True, blank=True, verbose_name="Thông tin mở rộng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="User"
    )

    class Meta:
        db_table = "account_user_info"
        verbose_name = "User info"
        verbose_name_plural = "Users info"

    def __str__(self):
        return self.full_name or '-'


class BlacklistToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    token = models.TextField()
    blacklisted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "account_blacklist_token"
        verbose_name = "Blacklist Token"
        verbose_name_plural = "Blacklist Token"

    @staticmethod
    def check_blacklist(user_id, auth_token):
        is_blacklist = BlacklistToken.objects.filter(user_id=user_id, token=auth_token).first()
        return True if is_blacklist else False

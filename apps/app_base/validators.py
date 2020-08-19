from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from commerce.settings.common import MAX_FILE_SIZE


def validate_file_extension_image(value):
    valid_extensions = ('.png', '.jpg', '.jpeg')
    if not value.name.lower().endswith(valid_extensions):
        raise ValidationError('File tải lên phải có định dạng là jpg, png hoặc jpeg')


def validate_image_size(value):
    file_size = value.size
    max_file_size = MAX_FILE_SIZE
    if file_size > max_file_size * 1024 * 1024:
        raise ValidationError("Dung lượng ảnh upload không được quá %sMB" % str(max_file_size))


def validate_email_field(value):
    validate_email(value)

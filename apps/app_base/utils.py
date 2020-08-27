import base64
import os
from cryptography.fernet import Fernet

from commerce.settings.common import ENCRYPT_KEY


def encrypt(string):
    try:
        cipher_suite = Fernet(ENCRYPT_KEY)
        encrypted_text = cipher_suite.encrypt(str(string).encode('UTF-8'))
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("UTF-8")
        return encrypted_text
    except Exception as e:
        print(e)
        return None


def decrypt(string):
    try:
        string = base64.urlsafe_b64decode(string)
        cipher_suite = Fernet(ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(string).decode("UTF-8")
        return decoded_text
    except Exception as e:
        print(e)
        return None


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

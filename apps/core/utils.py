from Crypto.Cipher import ARC4
from django.conf import settings
import base64


def encrypt(plaintext):
    cipher = ARC4.new(settings.SECRET_KEY)
    return base64.b64encode(cipher.encrypt(plaintext)).decode('utf-8')


def decrypt(ciphertext):
    cipher = ARC4.new(settings.SECRET_KEY)
    return cipher.decrypt(base64.b64decode(ciphertext)).strip()

from django.db import models
from django.conf import settings
from .cryptography import AESCipher

# Create your models here.


class EncryptedCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(EncryptedCharField, self).__init__(*args, **kwargs)
        self.encryptor = AESCipher(settings.ENCRYPT_SECRET_KEY)

    def get_prep_value(self, value):
        return encrypt_if_not_encrypted(value, self.encryptor)

    def to_python(self, value):
        return decrypt_if_not_decrypted(value, self.encryptor)


def encrypt_if_not_encrypted(value, encryptor):
    if isinstance(value, EncryptedString):
        return value
    else:
        encrypted = encryptor.encrypt(value)
        return EncryptedString(encrypted)


def decrypt_if_not_decrypted(value, encryptor):
    if isinstance(value, DecryptedString):
        return value
    else:
        encrypted = encryptor.decrypt(value)
        return DecryptedString(encrypted)


class EncryptedString(str):
    pass


class DecryptedString(str):
    pass


class Passport(models.Model):
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    middlename = models.CharField(max_length=32)
    phone = models.IntegerField()
    address = models.CharField(max_length=54)
    tin = EncryptedCharField(max_length=54)

    def __str__(self):
        return "%s - %s - %s" % (self.firstname, self.lastname, self.middlename)

    class Meta:
        db_table = "passport"

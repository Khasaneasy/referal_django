from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import random
import string


# генерация инвайт кода
def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        invite_code = generate_invite_code()
        user = self.model(
            phone_number=phone_number,
            invite_code=invite_code,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def activate_invite_code(self, invite_code):
        if not self.activated_invite_code:
            self.activated_invite_code = invite_code
            self.save()
            return True
        return False


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    activated_invite_code = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )
    invited_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_users'
    )
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

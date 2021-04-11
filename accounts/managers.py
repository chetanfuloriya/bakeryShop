from django.contrib.auth.models import BaseUserManager

from datetime import datetime


class UserManager(BaseUserManager):

    def _create_user(self, email, mobile, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = datetime.now()

        if not email and not mobile:
            raise ValueError('Email/mobile must be set for the user')

        email = self.normalize_email(email) if email else None
        user = self.model(
            email=email, mobile=mobile, last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, mobile=None, password=None,
                    **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, mobile, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have `is_staff = True`')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have `is_superuser = True`')

        return self._create_user(email, None, password, **extra_fields)

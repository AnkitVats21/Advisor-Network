from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

import os
import uuid

def image_upload(instance, filename):
    advisor_name = instance.advisor_name
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (advisor_name,uuid.uuid4(), ext)
    return os.path.join('uploads/advisorPhoto', filename)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name        = models.CharField(max_length=255)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    last_login  = models.DateTimeField(auto_now=True)
    date_joined = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):          
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Advisor(models.Model):
    """
    Advisor Model
    """
    
    advisor_name = models.CharField(max_length=255)
    advisor_photo = models.ImageField(upload_to=image_upload, max_length=1000)

    def __str__(self):
        return self.advisor_name
from django.db import models
# from django.contrib.auth.base_user import UserManager
from django.contrib.auth.models import AbstractBaseUser,UserManager
from django.utils.translation import gettext_lazy as _
import jwt
import datetime
from datetime import datetime,timedelta
from product_project import settings
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    category_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    status = models.BooleanField(default=True) 
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True,blank=True)


class adminManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class Admin(AbstractBaseUser, models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    mobilenumber = models.BigIntegerField(null=True,blank=True)
    password = models.CharField(
        max_length=255,null=True, blank=True)
    email = models.EmailField(
        _('email address'), blank=False, unique=True)
    
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = adminManager()

    @property
    def token(self):
        token = jwt.encode(
            {'id': self.id,
             'email': self.email,
                'mobile': self.mobilenumber,
                'exp': datetime.utcnow() + timedelta(days=365)},
            settings.SECRET_KEY, algorithm='HS256')

        return token

    

    def __str__(self):
        return self.name


class adminToken(models.Model):
    
    admin = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    authToken = models.TextField(null=True, blank=True)


# class Apikey(TrackingModel):
#     apikey = models.CharField(max_length=255)




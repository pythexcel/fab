from django.db import models
from fabapp.managers import UserManager
import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "User with this email already exists.",
        },
    )
    role = models.CharField(name="role", max_length=60)
    status = models.BooleanField(default=True)
    name = models.CharField(name="name", max_length=100)
    bio = models.TextField()
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    profile_image = models.ImageField(upload_to='Images/',
                                      default='Images/None/No-img.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'name', 'phone', 'bio']

    def __str__(self):
        return self.email


class Exhibition(models.Model):
    user = models.ForeignKey(User,
                             related_name='User',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    exhibition_name = models.CharField(max_length=350)


class Exhibitor(models.Model):
    exhibition = models.ForeignKey(Exhibition,
                                   related_name='exhibiton',
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             related_name='user',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    size = models.CharField(max_length=350)
    stall_no = models.CharField(max_length=350)
    color_theme = models.CharField(max_length=3000,null=True, blank=True)
    carpet = models.CharField(max_length=350)
    extra = models.CharField(max_length=3000,null=True, blank=True)
    website_link = models.URLField(max_length=350)
    created_on = models.DateTimeField(auto_now_add=True)


class ProductExhibitorDetail(models.Model):
    products = models.ForeignKey(Exhibitor,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    product = models.TextField()


class BrandingExhibitorDetail(models.Model):
    brandings = models.ForeignKey(Exhibitor,
                                  related_name='brandings',
                                  on_delete=models.CASCADE)
    branding = models.TextField()


class FurnitureExhibitorDetail(models.Model):
    furnitures = models.ForeignKey(Exhibitor,
                                   related_name='furnitures',
                                   on_delete=models.CASCADE)
    furniture = models.TextField()

class Portfolio(models.Model):
    user = models.ForeignKey(User,
                             related_name='fabricator_user',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images/',
                                      default='Images/None/No-img.jpg')

class ExhibitFab(models.Model):
    exhibition = models.ForeignKey(Exhibition,
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)

from django.utils import timezone
from django.db import models
from fabapp.managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin):
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
    cron_review = models.BooleanField(default=False)
    avg_rating = models.IntegerField(null=True,blank=True)

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
    Desciption = models.CharField(max_length=8000,null=True, blank=True)
    Start_date =  models.DateTimeField('start_date',default=timezone.now, blank=True) 
    end_date =  models.DateTimeField('end_date',default=timezone.now, blank=True)
    Running_status = models.BooleanField(default=True)

class ExhibitFab(models.Model):
    exhibition = models.ForeignKey(Exhibition,
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)

class AvailProd(models.Model):
    user = models.ForeignKey(User,
                             related_name='admin_prod',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    
    product = models.TextField()
    selected =  models.BooleanField(default=False)
    
class AvailBrand(models.Model):
    user = models.ForeignKey(User,
                             related_name='admin_brand',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    
    branding = models.TextField()
    selected =  models.BooleanField(default=False)

class AvailFurni(models.Model):
    user = models.ForeignKey(User,
                             related_name='admin_furni',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    furniture = models.TextField()
    selected =  models.BooleanField(default=False)
                         
    
    
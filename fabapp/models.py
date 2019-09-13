import uuid
from django.utils import timezone
from django.db import models
from fabapp.managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    profile_image = CloudinaryField('image')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    cron_review = models.BooleanField(default=False)
    avg_rating = models.IntegerField(null=True, blank=True)
    website_link = models.URLField(max_length=350, null=True, blank=True)
    fcm_token = models.CharField(max_length=200, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'name', 'phone', 'bio']

    def __str__(self):
        return self.email


class Exhibition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             related_name='User',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    exhibition_name = models.CharField(max_length=350)
    exhibition_image = CloudinaryField('image')
    Description = models.CharField(max_length=8000, null=True, blank=True)
    Start_date = models.DateTimeField('start_date',
                                      default=timezone.now,
                                      blank=True)
    end_date = models.DateTimeField('end_date',
                                    default=timezone.now,
                                    blank=True)
    Running_status = models.BooleanField(default=True)
    website_link = models.URLField(max_length=350, null=True, blank=True)


class ExhibitFab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exhibition = models.ForeignKey(Exhibition,
                                   blank=True,
                                   null=True,
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = (('exhibition', 'user'), )


class AvailProd(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             related_name='admin_prod',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)

    product = models.TextField()
    selected = models.BooleanField(default=False)


class AvailBrand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             related_name='admin_brand',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)

    branding = models.TextField()
    selected = models.BooleanField(default=False)


class AvailFurni(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             related_name='admin_furni',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    furniture = models.TextField()
    selected = models.BooleanField(default=False)



class Message(models.Model):
    sender = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='sender')
    receiver = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp', )

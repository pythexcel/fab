import uuid
from django.db import models
from fabapp.models import User, Exhibition


class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             related_name='fabricator_user',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images/',
                              default='Images/None/No-img.jpg')

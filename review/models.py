import uuid
from django.db import models
from fabapp.models import User

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,
                             related_name='mine_user',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    rated_user = models.ForeignKey(User,
                             related_name='rated_user',
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    
    comment = models.CharField(max_length=8000, null=True, blank=True)                
    rating = models.IntegerField(null=True,blank=True)
    
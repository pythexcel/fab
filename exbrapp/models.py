import uuid
from django.db import models
from fabapp.models import User, Exhibition


class Exhibitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    color_theme = models.CharField(max_length=3000, null=True, blank=True)
    carpet = models.CharField(max_length=350)
    extra = models.CharField(max_length=3000, null=True, blank=True)
    website_link = models.URLField(max_length=350)
    products = models.CharField(max_length=3000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class ProductExhibitorDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    products = models.ForeignKey(Exhibitor,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    product = models.TextField()
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return '%d: %s' % (self.quantity, self.product)


class BrandingExhibitorDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brandings = models.ForeignKey(Exhibitor,
                                  related_name='brandings',
                                  on_delete=models.CASCADE)
    branding = models.TextField()
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return '%d: %s' % (self.quantity, self.product)


class FurnitureExhibitorDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    furnitures = models.ForeignKey(Exhibitor,
                                   related_name='furnitures',
                                   on_delete=models.CASCADE)
    furniture = models.TextField()
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return '%d: %s' % (self.quantity, self.product)


class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fabs_user = models.ForeignKey(User,
                                 related_name='fabs_user',
                                 on_delete=models.CASCADE)
    mine_exhib = models.ForeignKey(Exhibitor,
                                 related_name='mine_exhib',
                                 on_delete=models.CASCADE)
    work_status = models.BooleanField(default=False)
    complete_status = models.BooleanField(default=False)
    response_status = models.BooleanField(default=False)
    comment = models.CharField(max_length=8000, null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        unique_together = (('fabs_user', 'mine_exhib'), )


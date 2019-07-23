from django.db import models
from fabapp.models import User, Exhibition


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
    color_theme = models.CharField(max_length=3000, null=True, blank=True)
    carpet = models.CharField(max_length=350)
    extra = models.CharField(max_length=3000, null=True, blank=True)
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

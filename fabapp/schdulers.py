from fabapp.models import User,Exhibition
from django.db.models import Q
from review.models import Review
from review.serializers import ReviewSeializer
from fabapp.serializers import UserDetailSerializer
from django.db.models import F, Sum, FloatField, Avg
from django.utils import timezone

def UserRating():
    print("User Rating schduler Running....")
    rv = User.objects.filter(cron_review=False,is_active=True,is_superuser=False,is_staff=False).first()
    if rv:
        rv.cron_review = True
        rv.save()
        serila = UserDetailSerializer(rv,many=False)
        ID = serila.data['id']
        us = Review.objects.filter(rated_user_id=ID).aggregate(total=Avg(F('rating')))
        rate = User.objects.get(id=ID)
        rate.avg_rating = us['total']
        rate.save()
        print('rating updated')    
    else:
        pass


def CronReset():
    rv = User.objects.filter(cron_review=True,is_active=True).update(cron_review=False)
    if rv:    
    else:
        pass        

def DisableExi():
    dis =  Exhibition.objects.filter(end_date__lt=timezone.now()).update(Running_status=False)
    if dis:
    else:
        pass



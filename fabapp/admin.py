from django.contrib import admin

from fabapp.models import User, Exhibition, Exhibitor
admin.site.register(User)
admin.site.register(Exhibition)
admin.site.register(Exhibitor)

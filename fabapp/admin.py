from django.contrib import admin
from fabapp.models import Exhibition,ExhibitFab,AvailBrand,AvailFurni,AvailProd,User,Exhibition
from exbrapp.models import Bid

admin.site.register(User)
admin.site.register(Exhibition)
admin.site.register(ExhibitFab)
admin.site.register(AvailBrand)
admin.site.register(AvailFurni)
admin.site.register(AvailProd)  
admin.site.register(Bid)

from django.contrib import admin
from fabapp.models import Exhibition, ExhibitFab, AvailBrand, AvailFurni, AvailProd, User, Exhibition
from exbrapp.models import Bid,Exhibitor


class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('exhibition_name', 'Start_date')
    list_filter = ('Start_date', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'phone', 'is_active')
    list_filter = ('role', )


class ProdAdmin(admin.ModelAdmin):
    list_display = ('product', )


class BrandAdmin(admin.ModelAdmin):
    list_display = ('branding', )


class FurniAdmin(admin.ModelAdmin):
    list_display = ('furniture', )


class ExhibitFabAdmin(admin.ModelAdmin):
    model = ExhibitFab
    list_display = ('user', 'get_name')

    def get_name(self, obj):
        return obj.exhibition.exhibition_name
    get_name.admin_order_field  = 'exhibition'  
    get_name.short_description = 'exhibition_name'  

class BidAdmin(admin.ModelAdmin):
    list_display = ('fabs_user','mine_exhib','work_status','complete_status','response_status')

admin.site.site_url = None
admin.site.register(User, UserAdmin)
admin.site.register(Exhibition, ExhibitionAdmin)
admin.site.register(ExhibitFab,ExhibitFabAdmin)
admin.site.register(AvailBrand, BrandAdmin)
admin.site.register(AvailFurni, FurniAdmin)
admin.site.register(AvailProd, ProdAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Exhibitor)

admin.site.site_header = 'Fabapp Administration'

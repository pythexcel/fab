from django.contrib import admin
from fabapp.models import Exhibition, ExhibitFab, AvailBrand, AvailFurni, AvailProd, User, Exhibition
from exbrapp.models import Bid,Exhibitor
from django.forms import ModelChoiceField
from django import forms

class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('exhibition_name', 'Start_date','end_date')
    list_filter = ('Start_date','end_date' )
    search_fields = ('exhibition_name',)



class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'phone', 'is_active')
    list_filter = ('role', )
    search_fields = ('email', 'name', 'phone', )


class ProdAdmin(admin.ModelAdmin):
    list_display = ('product', )
    search_fields = ('product',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('branding', )
    search_fields = ('branding',)

class FurniAdmin(admin.ModelAdmin):
    list_display = ('furniture', )
    search_fields = ('furniture',)

class ExhibitFabAdmin(admin.ModelAdmin):
    model = ExhibitFab
    fields = ('user','exhibition')
    raw_id_fields = ('exhibition','user')
    list_display = ('user', 'get_name')

    def get_name(self, obj):
        return obj.exhibition.exhibition_name
    get_name.admin_order_field  = 'exhibition'  
    get_name.short_description = 'exhibition_name'  



admin.site.site_url = None

admin.site.register(User, UserAdmin)
admin.site.register(Exhibition, ExhibitionAdmin)
admin.site.register(ExhibitFab,ExhibitFabAdmin)
admin.site.register(AvailBrand, BrandAdmin)
admin.site.register(AvailFurni, FurniAdmin)
admin.site.register(AvailProd, ProdAdmin)

admin.site.site_header = 'Fabapp Administration'



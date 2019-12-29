from django.contrib import admin
from django.contrib.auth.models import Group
from fabapp.models import Exhibition, ExhibitFab, AvailBrand, AvailFurni, AvailProd, User, Exhibition
from exbrapp.models import Bid, Exhibitor
from django.forms import ModelChoiceField
from django import forms
from rest_framework.authtoken.models import Token
from django_apscheduler.models import DjangoJob,DjangoJobExecution



class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('exhibition_name', 'Start_date', 'end_date','Running_status')
    list_filter = ('Start_date', 'end_date')
    search_fields = ('exhibition_name', )
    actions = ['Deactivate_exhibitions', ]


    def Deactivate_exhibitions(self, request, queryset):
        queryset.update(Running_status=False)
    Deactivate_exhibitions.short_description = "Mark selected exhibition as not working"
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'role', 'phone', 'is_active')
    list_filter = ('role', )
    list_display_links = ('company_name',)
    actions = ['Deactivate_user', ]
    search_fields = (
        'email',
        'company_name',
        'phone',
    )

    def Deactivate_user(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, '{} users have been disabled.'.format(count))
    Deactivate_user.short_description = "Mark selected users will be disabled"

class ProdAdmin(admin.ModelAdmin):
    list_display = ('product', )
    search_fields = ('product', )


class BrandAdmin(admin.ModelAdmin):
    list_display = ('branding', )
    search_fields = ('branding', )


class FurniAdmin(admin.ModelAdmin):
    list_display = ('furniture', )
    search_fields = ('furniture', )

class VideoDetailsInline(admin.TabularInline):
    model = User



class ExhibitFabAdmin(admin.ModelAdmin):
    model = ExhibitFab
    fields = ('user', 'exhibition')
    raw_id_fields = ('user', 'exhibition')
    list_display = ('user', 'get_name')

    def get_name(self, obj):
        return obj.exhibition.exhibition_name

    get_name.admin_order_field = 'exhibition'
    get_name.short_description = 'exhibition_name'



admin.site.register(User, UserAdmin)
admin.site.register(Exhibition, ExhibitionAdmin)
admin.site.register(ExhibitFab, ExhibitFabAdmin)
admin.site.register(AvailBrand, BrandAdmin)
admin.site.register(AvailFurni, FurniAdmin)
admin.site.unregister(Group)
admin.site.unregister(Token) 
admin.site.unregister(DjangoJob) 
admin.site.unregister(DjangoJobExecution) 



admin.site.site_url = None
admin.site.site_header = 'Fabapp Administration'

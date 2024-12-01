from django.contrib import admin
from .models import Cart,Tax
# Register your models here.
class CartAdminClass(admin.ModelAdmin):
    list_display=['user','fooditem','quantity','updated_at']

class TaxAdminClass(admin.ModelAdmin):
    list_display=('tax_type','tax_percentage','is_active')
    
admin.site.register(Cart,CartAdminClass)
admin.site.register(Tax,TaxAdminClass)
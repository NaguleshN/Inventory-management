from django.contrib import admin

from . models import Product,Cart,Category,Logs,Wastage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Logs)
admin.site.register(Wastage)


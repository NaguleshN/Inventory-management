from django.contrib import admin

from . models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Logs)
admin.site.register(Wastage)
admin.site.register(PurchasedItems)



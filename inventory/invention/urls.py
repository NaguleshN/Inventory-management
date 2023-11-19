from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home ,name="Home"), 
    path('about/', views.about , name="About"),


    #Product detail
    path('add_product/', views.add_product ,name="Add_product"), 
    path('add_category/', views.add_category, name="Add_category"),
    path('add_wastage/', views.add_wastage, name="Add_wastage"),
    path('logs/', views.logs, name="logs"),
    path('cart/', views.cart, name="cart"),
    path('product_description/<int:pk>', views.product_description, name="Product_description"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

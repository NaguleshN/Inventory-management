from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('complete/azuread-tenant-oauth2/home/', views.home ,name="Home"), 
    path('home/', views.home ,name="Home"), 
    path('about/', views.about , name="About"),


    #Product detail
    path('add_product/', views.add_product ,name="Add_product"), 
    path('add_category/', views.add_category, name="Add_category"),
    path('', views.login ,name="Login"), 
    path('register/', views.register ,name="Register"), 
    path('cart/', views.view_cart, name='view_cart'),
    path('logs/', views.logs, name="logs"),
    path('add_wastage/', views.add_wastage, name="Add_wastage"),
    path('add/<int:product_id>', views.add_to_cart, name="add_to_cart"),
    path('remove/<int:item_id>', views.remove_from_cart, name="remove_from_cart"),
    path('logout/', LogoutView.as_view() , name="logout"),
    path('product_description/<int:pk>', views.product_description, name="Product_description"),

    #admin
    path('admin_views/', views.admin_view, name='admin_views'),

    path('wastage_render/', views.wastage, name='wastage_render'),

    path('no_permisson/', views.no_permission, name='no_permission'),


    path('appoint_admin/<int:user_id>/', views.appoint_admin, name='appoint_admin'),
    path('remove_role/<int:user_id>/', views.remove_role, name='remove_role'),
    path('users/', views.users_list, name='users_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

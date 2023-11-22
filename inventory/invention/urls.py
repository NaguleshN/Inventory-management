from django.contrib import admin
from django.urls import path, include
from . import views
# from .views import cart_view


from django.conf import settings
from django.conf.urls.static import static

app_name = 'cart'

urlpatterns = [
    path('home/', views.home ,name="Home"), 
    path('about/', views.about , name="About"),

    #login
    path('', views.login_page, name="Login"),
    path('register/', views.register, name="Register"),


    #Product detail
    path('add_product/', views.add_product ,name="Add_product"), 
    path('add_category/', views.add_category, name="Add_category"),
    path('add_wastage/', views.add_wastage, name="Add_wastage"),

    #cart details
    path('cart/', views.cart, name='Cart'),
    # path('cart/<int:product_id>/', cart_view.as_view(), name='view_cart'),
    path('cart12/<int:item_id>/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('home/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

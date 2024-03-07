from django.contrib import admin
from django.urls import path,include
from food import views
from django.contrib.auth import views as auth_views
from food import views as user_views

urlpatterns = [
    path("",views.index,name='home'),
    path('Sign-up/',views.register,name = 'Sign-up'),
    path('Log-In/',views.login_request,name = 'Log-In'),
    path('order/',views.ordering,name='order'),
    path('search_order/',views.search_order,name='search-order'),
    path('product/<Restaurant__name>',views.product,name='product'),
    path('api/get/', user_views.api , name="api"),
    path('Logout/',user_views.logout_request,name="logout"),
    path('cart/',views.carts,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('admin_dashboard.html/',views.admin_dash,name="admin_dashboard"),

]

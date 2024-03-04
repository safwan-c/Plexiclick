from django.urls import path
from . import views
from .views import VariantPriceView,CartView,FavView
from django.views. decorators.csrf import csrf_exempt

 
urlpatterns= [
    path('',views.home,name="home"),
    path("shop", views.shop, name="shop"),
    
    path('register',views.register,name="register"),
    path('login/',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    
    path('cart/',views.cart_page,name="cart"),
    path('add_to_cart/', CartView.as_view()),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    
    path('favviewpage',views.favviewpage,name="fav"),
    path('add_to_fav/', FavView.as_view()),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    
    
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>/<str:product_id>',views.product_details,name="product_details"),
    
    path("checkout", views.checkout, name="checkout"),
    path("my_orders/", views.my_order, name="my_orders"),
    path("orderview/<str:pid>", views.orderview, name="orderview"),
    
    path("search/", views.search, name="Search"),
    path("about/", views.about, name="about"),
    path("cont", views.cont, name="cont"),
    
    
    path('basic/', VariantPriceView.as_view()),
    path('checkout/order', csrf_exempt (views.order), name='order'),

    
]
 
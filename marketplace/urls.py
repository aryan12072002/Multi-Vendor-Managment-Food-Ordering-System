from django.urls import path
from .views import marketplace,vendor_detail,add_to_cart,decrease_cart,cart,delete_cart
urlpatterns = [
    path("marketplace/",marketplace,name='marketplace'),
    path('<slug:vendor_slug>/',vendor_detail,name='vendor_detail'),
    #add to cart
    path('add_to_cart/<int:food_id>',add_to_cart,name='add_to_cart'),
    #decrease cart
    path('decrease_cart/<int:food_id>',decrease_cart,name='decrease_cart'),
    #delete  cart item
    path('delete_cart/<int:cart_id>',delete_cart,name='delete_cart'),
    
]
